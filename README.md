# manolAPP

Hau MANOLAK lagun taldeak erabiltzeko aplikazio bat da. 

## 1. Orrialdeak

### 1.1. Planak 

### 1.2. Gastuak 

### 1.3. BLOG 



## 2. Arkitektura eta Errendimendua

Script-ak sistemaren errendimendua zaintzeko diseinatuta dago:
* **Priority Management:** `nice` eta `ionice` komandoak erabiltzen ditu XMLak konprimitzerakoan, sistemaren beste prozesu batzuk ez moteltzeko.
* **Log Integratua:** Exekuzio bakoitzaren emaitza `config.cfg`-en zehaztutako karpetan gordetzen da.
* **Autokudeaketa:** Script-ak bere burua berriro programatzen du `at` komandoaren bidez, egunero 03:00etan exekutatu dadin.

## 3. Konfigurazioa (`config.cfg`)

Script-ak `/pseudo/backup_sistema/config/config.cfg` fitxategitik kargatzen ditu aldagaiak. 

> **Segurtasun oharra:** Ziurtatu fitxategi honek baimen murriztaileak dituela (`chmod 600 config.cfg`).

**Beharrezko aldagaiak:**
* `RUTA_BACKUP`: Kopia lokalak gordetzeko karpeta.
* `RUTA_XMLS`: XML jatorrizko karpeta.
* `DB_NAME`: Datu-basearen izena.
* `REMOTE_HOST`, `REMOTE_USER`, `REMOTE_PASS`, `REMOTE_PATH`: Urruneko zerbitzarirako sarbide datuak.

## 4. Arazoen Konponbidea

| Arazoa                   | Kausa posiblea                   | Konponbidea                                                    |
| :----------------------- | :------------------------------- | :------------------------------------------------------------- |
| **Transferentzia hutsa** | Urruneko zerbitzaria erorita     | Egiaztatu `lftp` konfigurazioa eta sareko konexioa.            |
| **Baimen akatsa**        | Scriptak ez du idazteko baimenik | Egiaztatu `chmod` eta `chown` baimenak `RUTA_BACKUP` karpetan. |
| **Ez da exekutatzen**    | `at` zerbitzua itzalita          | Exekutatu `systemctl start atd` eta `systemctl enable atd`.    |

## 5. Instalazioa eta Erabilera

### Exekuzio Manuala
Proba bat egiteko, exekutatu zuzenean:
```bash
/pseudo/backup_sistema/bin/backup_TBAI.sh

```

### Log-ak ikusteko

```bash
tail -f /pseudo/backup_sistema/logs/backup.log

```

## 6. Repositorioa eta Bertsio Kontrola

* **Repositorioa:** [https://github.com/nelizalde2026/manolAPP.git](https://github.com/nelizalde2026/manolAPP.git)
* **Adar nagusia:** `main`
* **Garapen adarrak:** `develop`


> **Garrantzitsua:**
> 1. Inoiz ez igo `.env` edo `.cfg` fitxategirik repositorio honetara. Aldaketa horiek tokikoak (lokalak) izan behar dira.
> 2. XMLak zip-atzerakoan, script-ak hiru direktorio baztertzen ditu (`tmp/`, `xsig/` eta `FACTURAS_ESPERA_CERTIFICADO/`). Egitura hau aldatzen bada, script-aren `zip` komandoaren `-x` parametroak eguneratu beharko dira.
> 
> 

```

```