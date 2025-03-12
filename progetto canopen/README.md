# Progetto per il file di test dell'inverter

Il file di test è `test_Inverter.py`

---

## Comandi per l'uso

### Avviare i test
```sh
python -m pytest test_Inverter.py
```

### Parametri opzionali

```sh
--interface (nome del tipo di interface che voglio usare, di default è messa a 'kvaser')

--channel (numero del canale su cui collegarsi, di default è messo a 0)

--bitrate (numero del bitrate per la connessione, di default è messo a 500000)

--start-index (index da cui partire per fare il loop finale di test, di default è messo a 0x2000)

--node-id (nodo della scheda da aggiungere al network, di default è messo a 113)
```



### Flashare sia master che slave e poi avviare i test
```sh
python -m pytest test_Inverter.py --flash --m "nome_file_master" --s "nome_file_slave"
```

### Fare il reboot e poi avviare i test
```sh
python -m pytest test_Inverter.py --reboot
```


