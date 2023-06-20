FROM python:3.11-alpine

RUN adduser -D sutekichan
RUN echo "export PATH=\"/home/sutekichan/.local/bin:$PATH\"" > /etc/profile.d/suteki_python_path.sh
ENV PATH=/home/sutekichan/.local/bin:$PATH

USER sutekichan
WORKDIR /home/sutekichan
RUN python3 -m pip install --user pipenv
COPY --chown=sutekichan:sutekichan src ./src
WORKDIR /home/sutekichan/src
RUN pipenv install

CMD ["pipenv", "run", "uvicorn","main:suteki"]