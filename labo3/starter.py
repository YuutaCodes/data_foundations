"""Data Foundations - Labo 2: Batch vs Streaming
Vul de TODO's aan. Gebruik Python 3.10 of hoger.
"""

import csv
import time
from collections import Counter
from datetime import datetime

DATA_FILE = "transacties.csv"
REPLAY_DELAY_SECONDS = 0.005
ALERT_THRESHOLD = 1000

# Returned een lijst van transacties
def load_rows(path=DATA_FILE):
    """Lees alle transacties in als dictionaries."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_transaction(row, seen_ids):
    """Controleer de kwaliteit van één transactie.

    Return:
        (cleaned_row, None) bij een geldige transactie
        (None, reden) bij een ongeldige transactie

    Regels:
    - transaction_id mag niet leeg of dubbel zijn.
    - timestamp moet een geldige ISO-datum zijn.
    - amount_eur moet een getal groter dan nul zijn.
    - status is 'approved' of 'declined'.
    - channel is 'web', 'app' of 'store'.

    Voeg een ID pas toe aan seen_ids wanneer alle
    controles succesvol zijn.
    """
    # TODO: implementeer alle validatieregels.

    if not row["transaction_id"]:
        return None, "transaction_id is empty"

    if row["transaction_id"] in seen_ids:
        return None, "transaction_id is double"

    if row["timestamp"]:
        try:
            datetime.fromisoformat(row["timestamp"])
        except ValueError:
            return None, "timestamp is not a valid ISO date"
    else:
        return None, "timestamp is empty"

    if not row["amount_eur"]:
        return None, "amount_eur is empty"

    try:
        row["amount_eur"] = float(row["amount_eur"])
    except ValueError:
        return None, "amount_eur is not a valid number"

    if row["amount_eur"] <= 0:
        return None, "amount_eur is not greater than zero"

    if row["status"] not in ["approved", "declined"]:
        return None, "status is not 'approved' or 'declined'"

    if row["channel"] not in ["web", "app", "store"]:
        return None, "channel is not 'web', 'app' or 'store'"    

    # Voeg de transaction_id pas toe aan seen_ids wanneer alle controles succesvol zijn.
    seen_ids.add(row["transaction_id"])

    # print(f"Valid transaction processed: {row['transaction_id']}")
    return row, None

def new_state():
    """Maak een lege verzameling resultaten."""
    return {
        "valid": 0,
        "invalid": 0,
        "revenue": 0.0,
        "approved_per_channel": Counter(),
        "alerts": [],
        "errors": [],
        "latencies_ms": [],
    }


def process_transaction(row, state, seen_ids):
    """Valideer en verwerk één transactie.

    - Houd geldige en ongeldige records bij.
    - Tel alleen goedgekeurde bedragen op als omzet.
    - Tel goedgekeurde transacties per kanaal.
    - Maak een alert voor goedgekeurde bedragen
      groter dan ALERT_THRESHOLD.
    - Bewaar de foutreden bij ongeldige records.
    """
    cleaned, reason = validate_transaction(row, seen_ids)

    if cleaned is None:
        state["invalid"] += 1
        state["errors"].append(reason)
        return

    state["valid"] += 1

    if cleaned["status"] != "approved":
        return

    state["revenue"] += cleaned["amount_eur"]
    state["approved_per_channel"][cleaned["channel"]] += 1

    if cleaned["amount_eur"] > ALERT_THRESHOLD:
        state["alerts"].append(cleaned["transaction_id"])


def run_batch(rows, batch_size=50):
    """Verwerk transacties in batches.

    Simuleer de aankomst van iedere transactie met
    REPLAY_DELAY_SECONDS.

    Bewaar per transactie het aankomstmoment.
    Verwerk een batch wanneer deze vol is.
    Verwerk ook de laatste, onvolledige batch.

    Meet de wachttijd vanaf aankomst tot verwerking.
    Geef de state terug.
    """
    # TODO: implementeer batchverwerking.

    # De eerste transactie van een batch wacht dus langer dan de laatste.
    # Dit komt omdat de eerste moet wachten tot de batch vol is voordat deze verwerkt wordt
    # De laatste transactie moet vrijwel niet wachten want deze wordt direct verwerkt.

    # Vraag: wat gebeurt er met de wachttijd als de batchgrootte groter wordt?
    # De wachttijd stijgt linear met de batchgrootte. Als de batchgrootte dubbel zo groot wordt, zal de wachttijd van totale batch ook verdubbelen.

    state = new_state()
    seen_ids = set()
    batch = []
    batchCounter = 1
    arrival = []

    def process_batch():
        print("Aankomst:")
        print(" ".join(arrival))
        print(f"Batch {batchCounter}:")
        print(f"[{', '.join(arrival)}]")
        for transaction, arrival_time in batch:
            process_transaction(transaction, state, seen_ids)
            state["latencies_ms"].append((time.perf_counter() - arrival_time) * 1000)
        batch.clear()
        arrival.clear()

    for number, row in enumerate(rows, start=1):
        time.sleep(REPLAY_DELAY_SECONDS)
        batch.append((row, time.perf_counter()))
        arrival.append(f"T{number}")

        if len(batch) == batch_size:
            process_batch()
            batchCounter += 1

    if batch:
        process_batch()

    return state


def run_streaming(rows):
    """Verwerk iedere transactie bij aankomst.

    Gebruik dezelfde aankomstvertraging als bij batch.
    Meet per transactie de verwerkingstijd vanaf
    het aankomstmoment.

    Geef de state terug.
    """
    # TODO: implementeer streamingverwerking.

    state = new_state()
    seen_ids = set()

    for row in rows:
        time.sleep(REPLAY_DELAY_SECONDS)
        arrival_time = time.perf_counter()
        process_transaction(row, state, seen_ids)
        state["latencies_ms"].append((time.perf_counter() - arrival_time) * 1000)

    return state

def print_summary(name, state):
    print(f"\n=== {name} ===")
    print("Geldig:", state["valid"])
    print("Ongeldig:", state["invalid"])
    print("Omzet:", round(state["revenue"], 2))
    print("Goedgekeurd per kanaal:", dict(state["approved_per_channel"]))
    print("Waarschuwingen:", state["alerts"])
    print("Fouten:", state["errors"])

    tijden = state["latencies_ms"]
    if tijden:
        print("Gemiddelde wachttijd (ms):", round(sum(tijden) / len(tijden), 2))


if __name__ == "__main__":
    rows = load_rows()
    
    print("Ingelezen transacties:", len(rows))

    

    # TODO: voer batchverwerking uit.
    batch_state = run_batch(rows)

    # TODO: voer streamingverwerking uit.
    streaming_state = run_streaming(rows)

    # TODO: toon beide samenvattingen.
    print_summary("Batchverwerking", batch_state)
    print_summary("Streamingverwerking", streaming_state)

    # TODO: controleer of beide methoden dezelfde
    #       inhoudelijke resultaten opleveren.
    assert batch_state["valid"] == streaming_state["valid"]
    assert batch_state["invalid"] == streaming_state["invalid"]

    assert abs(
        batch_state["revenue"] - streaming_state["revenue"]
    ) < 0.001

    assert batch_state["approved_per_channel"] == streaming_state["approved_per_channel"]
    assert sorted(batch_state["alerts"]) == sorted(streaming_state["alerts"])
    assert sorted(batch_state["errors"]) == sorted(streaming_state["errors"])
    assert batch_state["valid"] + batch_state["invalid"] == streaming_state["valid"] + streaming_state["invalid"] == len(rows)
