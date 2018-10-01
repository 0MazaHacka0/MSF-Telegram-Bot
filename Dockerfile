FROM python:3
ADD * /bot/

COPY /pymsf /bot/pymsf/

# Intstall pymsf requirements
RUN pip install -r /bot/pymsf/requirements.txt

# Install pymsf
RUN python /bot/pymsf/setup.py install

# Install bot requirements
RUN pip install -r /bot/requirements.txt

# Start bot
CMD [ "python", "./bot/bot.py" ]