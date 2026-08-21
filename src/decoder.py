import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from googlenewsdecoder import gnewsdecoder

def decode_rss_urls(df: pd.DataFrame, max_workers: int = 10) -> pd.DataFrame:
    def _decode(row):
        try:
            decoded = gnewsdecoder(row["link"], interval=0.2)
            real_url = decoded.get("decoded_url") if decoded.get("status") else None
        except Exception:
            real_url = None
        
        return {**row.to_dict(), "real_url": real_url}

    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(_decode, row) for _, row in df.iterrows()]
        for future in tqdm(as_completed(futures), total=len(futures), desc="Decoding Google News URLs"):
            results.append(future.result())

    return pd.DataFrame(results)
