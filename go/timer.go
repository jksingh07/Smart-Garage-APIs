package main

import (
  "os"
  "fmt"
  "time"
  "bytes"
  "strconv"
  "net/http"
  "io/ioutil"
  "encoding/json"
)

var car_id []string
var data map[string]Vehicle
var currentTime time.Time

var token string

var loginUrl = "http://4.229.225.201:5000/sim"
var poorHealthUrl = "http://4.229.225.201:5000/notify_poor_health?token="
var tiersUrl = "http://4.229.225.201:5000/notify_tiers?token="

var BRAKE_OIL = 40000
var AIR_FILTER = 15000

type Vehicle struct {
  CarID string `json:CarID`
  Milage int `json:Milage`
  LSDate string `json:LSDate`
  LSMilage int `json:LSMilage`
  OilType string `json:OilType`
  Tiers string `json:Tiers`
  AirFilter int `json:AirFilter`
  BrakeOil int `json:BrakeOil`
  LastestUpdate string `json:LastestUpdate`
}

func readDb() {
  wd, _:= os.Getwd()
  jsonFile, err := os.Open(wd + "/../db/car_db.json")
  if err != nil {
    fmt.Println(err)
  }
  fmt.Println("DB Read complete.... ")
  byteValue, _ := ioutil.ReadAll(jsonFile)
  json.Unmarshal(byteValue, &data)

  fmt.Println(data)
  defer jsonFile.Close()
}

// Runs forever untill the required data can be fetched
func check_timer(timer time.Time) {
  for {
    // Wait duration
    time.Sleep(10 * time.Second)

    // Check 1
    // Chck for the Tiers
    //
    mode := "Winter"
    cur_year := timer.Format("2006")
    max_limit,_ := time.Parse("02-01-2006", "01-10-" + cur_year)
    min_limit,_ := time.Parse("02-01-2006", "01-05-" + cur_year)
    //fmt.Println( "Max -> ", max_limit, timer.After(min_limit))
    //fmt.Println( "Min -> ", min_limit, timer.Before(max_limit))
    if (timer.After(min_limit) && timer.Before(max_limit)) {
      mode = "Summer"
    }
    for id := range car_id {
      current_tiers := data[car_id[id]].Tiers
      //fmt.Println( current_tiers, " -> ", mode)
      if (current_tiers == "All season") {
        continue
      }
      if (current_tiers != mode) {
        send_change_tiers_notification( car_id[id], mode)
        time.Sleep(2 * time.Second)
      }
    }

    // Check 2
    // Chck for the Service Data
    //
    for id := range car_id {
      curr_car := data[car_id[id]]
      driven := curr_car.Milage - curr_car.LSMilage
      time_ls,_ := time.Parse("02-01-2006", curr_car.LSDate)
      time_lu,_ := time.Parse("02-01-2006", curr_car.LastestUpdate)
      days := time_lu.Sub(time_ls).Hours()
      if (days < 1) {
        days = 1
      }
      avg := float64(driven)/days * 24
      fmt.Println(curr_car.CarID, driven, " km in ", days/24, avg)

      // Check Engine oil
      oilLimit := get_oil_limit(curr_car.OilType)
      oilLimitOg := get_oil_limit_org(curr_car.OilType)
      health := float64(driven)/float64(oilLimitOg)
      h_str := strconv.FormatFloat(health, 'g', 5, 64)
      if (driven > oilLimit) {
        send_poor_health_notification(car_id[id], "Engine oil", h_str)
        time.Sleep(2 * time.Second)
      }

      // Check Brake oil
      driven = curr_car.Milage - curr_car.BrakeOil
      health = float64(driven)/float64(BRAKE_OIL)
      h_str = strconv.FormatFloat(health, 'g', 5, 64)
      if (driven + 1000 > BRAKE_OIL) {
        send_poor_health_notification(car_id[id], "Brake oil", h_str)
        time.Sleep(2 * time.Second)
      }

      // Check Air filter
      driven = curr_car.Milage - curr_car.AirFilter
      health = float64(driven)/float64(AIR_FILTER)
      h_str = strconv.FormatFloat(health, 'g', 5, 64)
      if (driven + 1000 > AIR_FILTER) {
        send_poor_health_notification(car_id[id], "AirFilter", h_str)
        time.Sleep(2 * time.Second)
      }
    }

  }
}

func get_oil_limit(oiltype string) int{
  switch (oiltype) {
  case "TYPE C":
    return 12000
  case "TYPE B":
    return 9000
  default:
    return 5000
  }
}

func get_oil_limit_org(oiltype string) int{
  switch (oiltype) {
  case "TYPE C":
    return 16000
  case "TYPE B":
    return 11000
  default:
    return 6500
  }
}

func send_change_tiers_notification(id string, mode string) {
  fmt.Println("Change Tiers :-> ", id, mode)
  values := map[string]string{"CarID": id, "Tiers": mode}
  jsonValue, _ := json.Marshal(values)

  resp, _ := http.Post(tiersUrl + token, "application/json", bytes.NewBuffer(jsonValue))
  fmt.Println(resp)
}

func send_poor_health_notification(id string, component string, health string) {
  fmt.Println("Poor Health :-> ", id, component, health)
  values := map[string]string{"CarID": id, "Component": component, "Health":health}
  jsonValue, _ := json.Marshal(values)

  resp, _ := http.Post(poorHealthUrl + token, "application/json", bytes.NewBuffer(jsonValue))
  fmt.Println(resp)
}

func get_token() {
  // values := map[string]string{"email": "admin@a.com", "password": "admin"}
  // jsonValue, _ := json.Marshal(values)

  resp, _ := http.Get(loginUrl)
  defer resp.Body.Close()
  decoder := json.NewDecoder(resp.Body)
  var data map[string]string
  _ = decoder.Decode(&data)
  token = data["token"]
  fmt.Println(data["token"])
}

func main() {
  currentTime = time.Now()
  //currentTime,_ = time.Parse("02-01-2006", "02-05-2022")

  readDb()
  car_id = make([]string, 0, len(data))
  for key, _ := range data {
    car_id = append(car_id, key)
    //fmt.Println("CarIds ", key)
  }
  get_token()
  go check_timer(currentTime)
  for {
    time.Sleep(20 * time.Second)
    fmt.Println("Main running.")
  }
}
