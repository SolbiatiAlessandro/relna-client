# relna-client

This is the command-line client interface for relna

## relna-client APIs

```
(venv) python relna.py --command fork 
```
- [X] Implemented
`relna fork` allows you to fork a trainer from relna. It will download and unzip a trainer package from the relna backend.
The trainer package will have a `model.py` that you can work on.

```
relna data
```
- [ ] Implemented
Data are supposed to be in the cloud, but you can request a local copy for experimentation. You will recieve only a small amount of the data to make fast iterations.

```
relna check
```
- [ ] Implemented
`relna check` run the built-in trainer (unit and integration) test suite to validate your trainer before shipping. If the trainer doesn't pass the `check` than it won't ship.


```
(venv) python relna.py --command ship 
```
- [X] Implemented
`relna ship` ships the trainer to the relna backend 
