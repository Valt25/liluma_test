docker build -f ./bot/deploy/main/Dockerfile -t local/liluma_test_bot:latest ./bot
docker build -f ./bot/deploy/updater/Dockerfile -t local/liluma_test_updater:latest ./bot
