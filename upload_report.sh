if [[ `git status --porcelain` ]]; then
   echo "# New Changes Found"
   git add .
   git commit -m "Jenkins: Updated Lastest Build Report"
   git push -u origin HEAD:main
else
   echo "# No changes"
fi
