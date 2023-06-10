# Suteki-chan
Suteki Chan consumes payloads from GitLab and sends a message to Slack based on a predetermined set of rules.

## How it works

Suteki-chan is based on FastAPI and utilizes pydantic to build the data models.
It listens for incoming payloads from GitLab (more to be added) and executes actions depending on your configuration.

## Configuration

Suteki-chan is easy to use and easy to configure.
You need to create a `config.yaml` file (or use any name, i.e. `suteki.yaml`) and set `SUTEKI_CONFIG` environmental
variable to the path of that file.

Full config file reference:

```yaml
version: 0.1.0
security:
  token: "Gitlab Verification Token"
jobs:
  - name: "Send a message to slack"
    rules:
      - model.type == "Push Hook"
    actions:
      - name: Post a message to the channel
        module: slack
        action: post_message
        args:
          channel: D0000000000
          message: "Suteki-chan says NYA!"
        output: result
```

### `version`
This is optional, although this is like the subject to change. You are advised to use it.

### `security.token`
This is the secret token [as described by GitLab](https://docs.gitlab.com/ee/user/project/integrations/webhooks.html#validate-payloads-by-using-a-secret-token).

### `jobs`
The list of jobs to be executed whenever a valid payload is received by Suteki-chan.

### `jobs.name` [Optional]
A name of the job to help you identify and maintain the configuration file later.

### `jobs.rules` [Optional]
A list of rules. If you don't specify `jobs.rules`, Suteki-chan assumes you want to execute it every time a valid payload arrives.

You may specify as many rules as you want in a form of a list. Use standard Python syntax when you do.
Suteki-chan evaluates every rule one by one and the first rule that evaluates as `True` will execute the job.

If you specify `jobs.rules` and no rule is evaluated as `True`, the job is not executed.

### `actions`
A list of actions to take.

### `actions.name` [Optional]
A name of the action to help you identify and maintain the configuration file later.

### `actions.module`
The name of the module to call.
Right now, only `slack` is available. Read the documentation on `builtins.slack` module to learn more.

### `actions.action`
The name of the method to call inside the loaded module.

### `actions.args` [Optional]
A list of arguments to use in the called method. Some modules require arguments to be set, some do not. Read the module documentation for more information.

### `actions.output` [Optional]
The name of the variable to store output in.

To use the variable, call `output.variable_name` later on. You can use this variable across all jobs.

Example:
```yaml
    actions:
      - module: slack
        action: post_message
        args:
          channel: D0000000000
          message: "Suteki-chan says NYA!"
        output: thread_id
      - module: slack
        action: post_message
        args:
          channel: D0000000000
          thread: output.thread_id
          message: "Suteki-chan says NYA!"
```
This will first post a message into a channel and then post another one into it's thread.

## Running Suteki-chan
To start Suteki-chan, execute

```bash
uvicorn main:suteki
```
