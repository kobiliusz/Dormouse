pip3 install -r requirements.txt
if test -f "./instance/dormouse.db"; then
  rm ./instance/dormouse.db
fi
python3 db.py
cd static
npm run build
