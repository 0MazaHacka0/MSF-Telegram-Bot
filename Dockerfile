FROM python:3
ADD * /bot/

ADD /pymsf /pymsf/

# Install bot requirements
RUN pip install -r /bot/requirements.txt

# Intstall pymsf requirements
RUN pip install -r /bot/pymsf/requirements.txt

# Install pymsf
RUN python /bot/pymsf/setup.py install

# Start bot
CMD [ "python", "./bot/bot.py" ]