if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Thorappan-TG/Professor-Bot.git /Professor-Bot
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /Professor-Bot
fi
cd /Ajax
pip3 install -U -r requirements.txt
echo "Starting 𝙼𝙺𝙽 𝙱𝙾𝚃𝚉....🔥"
python3 bot.py
