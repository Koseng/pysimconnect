from simconnect import (
    SimConnect, OBJECT_ID_USER,
    GROUP_PRIORITY_HIGHEST, EVENT_FLAG_GROUPID_IS_PRIORITY,
)

event = 'KOHLSMAN_INC'
data = 0        # some events take an argument, not required here

with SimConnect(name='SendEvent') as sc:
    client_id = sc.EVENTS.get(event, {}).get('client_id')
    assert client_id, f"unrecognized event {event}"
    sc.MapClientEventToSimEvent(client_id, event)

    # click up the altimeter setting a few times
    for _ in range(10):
        print(f"Sending {event} event")
        sc.TransmitClientEvent(
            OBJECT_ID_USER,
            client_id,
            data,
            GROUP_PRIORITY_HIGHEST,
            EVENT_FLAG_GROUPID_IS_PRIORITY,
        )

    for _ in range(10):
        # see what comes back...
        recv = sc.receiveNext(timeout_seconds=0.5)
        print(f"Got {recv.__class__.__name__ if recv else 'nothing'}...")
