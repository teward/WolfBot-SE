# WolfBot-SE
A chatbot for StackExchange

This is a very simple little chatbot for StackExchange stuff. It features a very simple plugin system that allows users to add new commands and tasks with absolute ease.

## Setting Up

1. Install all dependencies:

```
pip install beautifulsoup4
pip install websocket-client
```    
    
2. Run `python WolfCore.py`
3. Enter credentials and room number
4. Navigate to the room, and paste in superuser escalation command (`/iamthecaptainnow FFFFFF`)

## Accounts

You will need a StackExchange account with at least 20 reputation. You may not use OpenID at this time -- you *must* use an e-mail address through SE's login system. Additionally, you also need to sign on at http://stackexchange.com/ at least once before being able to connect to any chat rooms.

## Plugins

1. Create a new plugin under the `plugins/` folder in the main directory.
2. Add your code to it. Use the `AUPlugin.py` file as an example.
3. Restart the bot to load the new plugin.
