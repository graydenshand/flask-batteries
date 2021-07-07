{{ (name[0]|upper) + name[1:] }}

Created by Flask-Batteries

# Getting Started
Flask-Batteries uses Webpack, a NodeJS asset manager to build a minified bundle for static assets. 

You must have npm and npx installed before using. Check if you have them installed by calling:
```bash
npm -v && npx -v
#7.11.2
#7.11.2
```
If you do not already have them installed, follow the guides below:
* [Installing npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
* [Installing npx](https://www.npmjs.com/package/npx)

Now that you have npm installed, install the project dependencies with: 
```bash
npm install
```

Next, activate your virtual python environment:
```bash
source venv/bin/activate
```

Finally, start the app by calling:
```bash
flask run
```

The app runs on port 5000 by default, to see it visit https://127.0.0.1:5000 in your browser.