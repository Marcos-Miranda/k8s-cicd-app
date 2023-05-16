# k8s-cicd-app

The game Civilization 6 has a asynchronous multiplayer mode, where the players don't need to be online at the same time, they take their turn when it's best suited and the game save the state to the cloud. The game has a Webhook feature that sends a POST request to the endpoint you set every time is someone's turn. The request has the following body:

```json
{
    "value1": "name of the game",
    "value2": "name of the player",
    "value3": "turn number"
}
```

This project consists of a Web app that listens to this Webhook and sends a notification to a given Telegram chat, informing a player that it's his turn on the game. 

There is a full CI/CD pipeline implemented, utilizing GCP Cloud Build. When a commit is made to the main branch the build phase is triggered, which runs linting and unit tests, build the app's docker image and push it to the artifact repository. When a tag is pushed to the git repository the deploy phase is triggered, which deploy the application to Google Kubernetes Engine (GKE).