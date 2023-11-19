from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rethinkdb import r
from django.conf import settings
from django.http import HttpResponseServerError
import json

# Defina as constantes do RethinkDB
RETHINKDB_HOST = '200.17.86.19'
RETHINKDB_PORT = 58015
RETHINKDB_DB = 'santa_rosa'
RETHINKDB_USER = 'theodoro.ferreira@sou.unijui.edu.br'
RETHINKDB_PASSWORD = 'DS3hs7k28fj'

# Armazene os clientes que aguardam atualizações
clients = []

def micropar(request):
    conexao = r.connect(
        host=RETHINKDB_HOST,
        port=RETHINKDB_PORT,
        db=RETHINKDB_DB,
        user=RETHINKDB_USER,
        password=RETHINKDB_PASSWORD
    )

    try:
        microparticulas = list(r.table('microparticulas').run(conexao))

        latest_data = []
        for micropart in microparticulas:
            if clients:
                send_update({
                    'latest_data': [
                        micropart['id'],
                        micropart['devAddr'],
                        micropart['deviceInfo']['deviceName'],
                        float(micropart['object']['temperature']),
                        float(micropart['object']['humidity']),
                        float(micropart['object']['pm2_5']),
                        float(micropart['object']['noise']),
                        float(micropart['object']['voltage']),
                        micropart['time'],
                        {
                            "applicationId": micropart['deviceInfo']['applicationId'],
                            "applicationName": micropart['deviceInfo']['applicationName'],
                            "devEui": micropart['deviceInfo']['devEui'],
                            "deviceName": micropart['deviceInfo']['deviceName'],
                            "deviceProfileId": micropart['deviceInfo']['deviceProfileId'],
                            "deviceProfileName": micropart['deviceInfo']['deviceProfileName'],
                            "tags": micropart['deviceInfo'].get('tags', {}),
                            "tenantId": micropart['deviceInfo']['tenantId'],
                            "tenantName": micropart['deviceInfo']['tenantName']
                        },
                        {
                            str(i): {
                                "channel": info.get('channel', ''),
                                "context": info.get('context', ''),
                                "crcStatus": info.get('crcStatus', ''),
                                "gatewayId": info.get('gatewayId', ''),
                                "location": info.get('location', {}),
                                "metadata": info.get('metadata', {}),
                                "rfChain": info.get('rfChain', ''),
                                "rssi": info.get('rssi', ''),
                                "snr": info.get('snr', ''),
                                "time": info.get('time', ''),
                                "timeSinceGpsEpoch": info.get('timeSinceGpsEpoch', ''),
                                "uplinkId": info.get('uplinkId', '')
                            } for i, info in enumerate(micropart['rxInfo'])
                        }
                    ],
                    'status': 'success'
                })

            data_entry = [
                micropart['id'],
                micropart['devAddr'],
                micropart['deviceInfo']['deviceName'],
                float(micropart['object']['temperature']),
                float(micropart['object']['humidity']),
                float(micropart['object']['pm2_5']),
                float(micropart['object']['noise']),
                float(micropart['object']['voltage']),
                micropart['time'],
                {
                    "applicationId": micropart['deviceInfo']['applicationId'],
                    "applicationName": micropart['deviceInfo']['applicationName'],
                    "devEui": micropart['deviceInfo']['devEui'],
                    "deviceName": micropart['deviceInfo']['deviceName'],
                    "deviceProfileId": micropart['deviceInfo']['deviceProfileId'],
                    "deviceProfileName": micropart['deviceInfo']['deviceProfileName'],
                    "tags": micropart['deviceInfo'].get('tags', {}),
                    "tenantId": micropart['deviceInfo']['tenantId'],
                    "tenantName": micropart['deviceInfo']['tenantName']
                },
                {
                    str(i): {
                        "channel": info.get('channel', ''),
                        "context": info.get('context', ''),
                        "crcStatus": info.get('crcStatus', ''),
                        "gatewayId": info.get('gatewayId', ''),
                        "location": info.get('location', {}),
                        "metadata": info.get('metadata', {}),
                        "rfChain": info.get('rfChain', ''),
                        "rssi": info.get('rssi', ''),
                        "snr": info.get('snr', ''),
                        "time": info.get('time', ''),
                        "timeSinceGpsEpoch": info.get('timeSinceGpsEpoch', ''),
                        "uplinkId": info.get('uplinkId', '')
                    } for i, info in enumerate(micropart['rxInfo'])
                }
            ]
            latest_data.append(data_entry)

        data = {'latest_data': latest_data, 'status': 'success'}

    except Exception as e:
        return JsonResponse({'error': str(e)})

    json_dumps_params = {'indent': 2, 'ensure_ascii': False}

    return JsonResponse(data, json_dumps_params=json_dumps_params, safe=False)

@csrf_exempt
def dados_json(request):
    conexao = r.connect(
        host=RETHINKDB_HOST,
        port=RETHINKDB_PORT,
        db=RETHINKDB_DB,
        user=RETHINKDB_USER,
        password=RETHINKDB_PASSWORD
    )

    try:
        pessoas = list(r.table('estacoes_metereologicas').run(conexao))

        latest_data = []
        for pessoa in pessoas:
            # Se houver clientes esperando, envie atualizações
            if clients:
                send_update({
                    'latest_data': [
                        pessoa['id'],
                        pessoa['devAddr'],
                        pessoa['deviceInfo']['deviceName'],
                        float(pessoa['object']['internal_sensors'][0]['v']),
                        float(pessoa['object']['internal_sensors'][1]['v']),
                        float(pessoa['object']['modules'][1]['v']),
                        float(pessoa['object']['modules'][3]['v']),
                        float(pessoa['object']['modules'][8]['v']),
                        pessoa['time'],
                        {
                            "applicationId": pessoa['deviceInfo']['applicationId'],
                            "applicationName": pessoa['deviceInfo']['applicationName'],
                            "devEui": pessoa['deviceInfo']['devEui'],
                            "deviceName": pessoa['deviceInfo']['deviceName'],
                            "deviceProfileId": pessoa['deviceInfo']['deviceProfileId'],
                            "deviceProfileName": pessoa['deviceInfo']['deviceProfileName'],
                            "tags": pessoa['deviceInfo'].get('tags', {}),
                            "tenantId": pessoa['deviceInfo']['tenantId'],
                            "tenantName": pessoa['deviceInfo']['tenantName']
                        },
                        {
                            str(i): {
                                "channel": info.get('channel', ''),
                                "context": info.get('context', ''),
                                "crcStatus": info.get('crcStatus', ''),
                                "gatewayId": info.get('gatewayId', ''),
                                "location": info.get('location', {}),
                                "metadata": info.get('metadata', {}),
                                "rfChain": info.get('rfChain', ''),
                                "rssi": info.get('rssi', ''),
                                "snr": info.get('snr', ''),
                                "time": info.get('time', ''),
                                "timeSinceGpsEpoch": info.get('timeSinceGpsEpoch', ''),
                                "uplinkId": info.get('uplinkId', '')
                            } for i, info in enumerate(pessoa['rxInfo'])
                        }
                    ],
                    'status': 'success'
                })

            data_entry = [
                pessoa['id'],
                pessoa['devAddr'],
                pessoa['deviceInfo']['deviceName'],
                float(pessoa['object']['internal_sensors'][0]['v']),
                float(pessoa['object']['internal_sensors'][1]['v']),
                float(pessoa['object']['modules'][1]['v']),
                float(pessoa['object']['modules'][3]['v']),
                float(pessoa['object']['modules'][8]['v']),
                pessoa['time'],
                {
                    "applicationId": pessoa['deviceInfo']['applicationId'],
                    "applicationName": pessoa['deviceInfo']['applicationName'],
                    "devEui": pessoa['deviceInfo']['devEui'],
                    "deviceName": pessoa['deviceInfo']['deviceName'],
                    "deviceProfileId": pessoa['deviceInfo']['deviceProfileId'],
                    "deviceProfileName": pessoa['deviceInfo']['deviceProfileName'],
                    "tags": pessoa['deviceInfo'].get('tags', {}),
                    "tenantId": pessoa['deviceInfo']['tenantId'],
                    "tenantName": pessoa['deviceInfo']['tenantName']
                },
                {
                    str(i): {
                        "channel": info.get('channel', ''),
                        "context": info.get('context', ''),
                        "crcStatus": info.get('crcStatus', ''),
                        "gatewayId": info.get('gatewayId', ''),
                        "location": info.get('location', {}),
                        "metadata": info.get('metadata', {}),
                        "rfChain": info.get('rfChain', ''),
                        "rssi": info.get('rssi', ''),
                        "snr": info.get('snr', ''),
                        "time": info.get('time', ''),
                        "timeSinceGpsEpoch": info.get('timeSinceGpsEpoch', ''),
                        "uplinkId": info.get('uplinkId', '')
                    } for i, info in enumerate(pessoa['rxInfo'])
                }
            ]
            latest_data.append(data_entry)

        data = {'latest_data': latest_data, 'status': 'success'}

    except Exception as e:
        return JsonResponse({'error': str(e)})

    json_dumps_params = {'indent': 2, 'ensure_ascii': False}

    return JsonResponse(data, json_dumps_params=json_dumps_params, safe=False)

def send_update(data):
    for client in clients:
        try:
            # Envie os dados para o cliente
            client.write_message(json.dumps(data))
        except:
            # Se houver algum problema, remova o cliente
            clients.remove(client)

@csrf_exempt
def dados_json_update(request):
    if request.method == 'POST':
        # Registre o cliente para atualizações
        clients.append(request.websocket)
        return JsonResponse({'status': 'success'})
    else:
        return HttpResponseServerError("Method not allowed")

def gb_tracker(request):
    conexao = r.connect(
        host=RETHINKDB_HOST,
        port=RETHINKDB_PORT,
        db=RETHINKDB_DB,
        user=RETHINKDB_USER,
        password=RETHINKDB_PASSWORD
    )

    try:
        pessoas = list(r.table('gb_tracker').run(conexao))

        latest_data = []
        for pessoa in pessoas:
            formatted_person = {
                'latest_data': [
                    pessoa['id'],
                    pessoa['devAddr'],
                    pessoa['deviceInfo']['deviceName'],
                    float(pessoa['object']['altitude']),
                    float(pessoa['object']['lat']),
                    float(pessoa['object']['lon']),
                    float(pessoa['object']['satelites']),
                    float(pessoa['object']['temperatura']),
                    float(pessoa['object']['umidade']),
                    pessoa['time'],
                    {
                        "applicationId": pessoa['deviceInfo']['applicationId'],
                        "applicationName": pessoa['deviceInfo']['applicationName'],
                        "devEui": pessoa['deviceInfo']['devEui'],
                        "deviceName": pessoa['deviceInfo']['deviceName'],
                        "deviceProfileId": pessoa['deviceInfo']['deviceProfileId'],
                        "deviceProfileName": pessoa['deviceInfo']['deviceProfileName'],
                        "tags": pessoa['deviceInfo'].get('tags', {}),
                        "tenantId": pessoa['deviceInfo']['tenantId'],
                        "tenantName": pessoa['deviceInfo']['tenantName']
                    },
                    {
                        str(i): {
                            "channel": info.get('channel', ''),
                            "context": info.get('context', ''),
                            "crcStatus": info.get('crcStatus', ''),
                            "gatewayId": info.get('gatewayId', ''),
                            "location": info.get('location', {}),
                            "metadata": info.get('metadata', {}),
                            "rfChain": info.get('rfChain', ''),
                            "rssi": info.get('rssi', ''),
                            "snr": info.get('snr', ''),
                            "time": info.get('time', ''),
                            "timeSinceGpsEpoch": info.get('timeSinceGpsEpoch', ''),
                            "uplinkId": info.get('uplinkId', '')
                        } for i, info in enumerate(pessoa['rxInfo'])
                    }
                ],
                'status': 'success'
            }

            data_entry = [
                pessoa['id'],
                pessoa['devAddr'],
                pessoa['deviceInfo']['deviceName'],
                float(pessoa['object']['altitude']),
                float(pessoa['object']['lat']),
                float(pessoa['object']['lon']),
                float(pessoa['object']['satelites']),
                float(pessoa['object']['temperatura']),
                float(pessoa['object']['umidade']),
                pessoa['time'],
                {
                    "applicationId": pessoa['deviceInfo']['applicationId'],
                    "applicationName": pessoa['deviceInfo']['applicationName'],
                    "devEui": pessoa['deviceInfo']['devEui'],
                    "deviceName": pessoa['deviceInfo']['deviceName'],
                    "deviceProfileId": pessoa['deviceInfo']['deviceProfileId'],
                    "deviceProfileName": pessoa['deviceInfo']['deviceProfileName'],
                    "tags": pessoa['deviceInfo'].get('tags', {}),
                    "tenantId": pessoa['deviceInfo']['tenantId'],
                    "tenantName": pessoa['deviceInfo']['tenantName']
                },
                {
                    str(i): {
                        "channel": info.get('channel', ''),
                        "context": info.get('context', ''),
                        "crcStatus": info.get('crcStatus', ''),
                        "gatewayId": info.get('gatewayId', ''),
                        "location": info.get('location', {}),
                        "metadata": info.get('metadata', {}),
                        "rfChain": info.get('rfChain', ''),
                        "rssi": info.get('rssi', ''),
                        "snr": info.get('snr', ''),
                        "time": info.get('time', ''),
                        "timeSinceGpsEpoch": info.get('timeSinceGpsEpoch', ''),
                        "uplinkId": info.get('uplinkId', '')
                    } for i, info in enumerate(pessoa['rxInfo'])
                }
            ]
            latest_data.append(data_entry)

        data = {'latest_data': latest_data, 'status': 'success'}

    except Exception as e:
        return JsonResponse({'error': str(e)})

    json_dumps_params = {'indent': 2, 'ensure_ascii': False}

    return JsonResponse(data, json_dumps_params=json_dumps_params, safe=False)
