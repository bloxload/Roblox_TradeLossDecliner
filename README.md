# AutoLossDecliner
Automatically declines trades set at a threshold, uses 1 ratio.

## How to run

You need Python installed, preferably the lastest version.

Open command prompt and navigate to the folder.

Run it with 
```
py main.py
```

## Errors

`KeyError: 'data'`
`line 52, in <module>`

Your ROBLOSECURITY is invalid.

## Functionality

Checks trade every 60 seconds, checks the loss to win ratio and declines if below threshold.
