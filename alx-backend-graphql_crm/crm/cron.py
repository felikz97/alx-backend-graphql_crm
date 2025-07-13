def update_low_stock():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        response = requests.post('http://localhost:8000/graphql', json={
            'query': 'mutation { updateLowStockProducts { products { name stock } message } }'
        })
        if response.status_code == 200:
            data = response.json()
            lines = [f"{timestamp} - {p['name']} restocked to {p['stock']}" for p in data['data']['updateLowStockProducts']['products']]
            with open('/tmp/low_stock_updates_log.txt', 'a') as f:
                f.write("\n".join(lines) + "\n")
        else:
            raise Exception("Bad response")
    except Exception as e:
        with open('/tmp/low_stock_updates_log.txt', 'a') as f:
            f.write(f"{timestamp} - Error: {e}\n")

