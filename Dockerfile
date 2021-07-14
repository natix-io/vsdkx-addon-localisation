#FROM 212730513262.dkr.ecr.eu-central-1.amazonaws.com/arm:latest
FROM 212730513262.dkr.ecr.eu-central-1.amazonaws.com/cardetection:latest
ADD ./ /app
WORKDIR /app
# get git to install custom pip package
RUN apt-get update && apt-get install -y git
# comment next line if you do not have requirements
RUN python3.7 -m pip install --ignore-installed -r ./conda_requirements.txt
RUN chmod 777 start.sh
