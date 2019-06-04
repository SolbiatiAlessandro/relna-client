# relna-client

This is the command-line client interface for relna

## relna-client APIs

```
relna fork <trainer-hash>
```

`relna fork` allows you to fork a trainer from relna. It will download and unzip a trainer package from the relna backend.
The trainer package will have a `model.py` that you can work on.

```
relna data

Data are supposed to be in the cloud, but you can request a local copy for experimentation. You will recieve only a small amount of the data to make fast iterations.

```
relna check
```
`relna check` run the built-in trainer (unit and integration) test suite to validate your trainer before shipping. If the trainer doesn't pass the `check` than it won't ship.


```
relna ship
```
`relna ship` ships the trainer to the relna backend 
