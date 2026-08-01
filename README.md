# invasive_species_detection
ML model to detect and classify invasive species

## Extract a frame from a video

A small utility is included at `scripts/extract_frame.py` to extract every 100th frame from a video by time (seconds) or by frame index.

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Examples (PowerShell):

```powershell
# extract frame at 12.5 seconds
python scripts\extract_frame.py --video C:\path\to\video.mp4 

```

## Install POSTGIS in docker.
```
docker run --name invasive_db -e POSTGRES_PASSWORD=Shriya2008 -p 5432:5432 -v "C:\Venky\invasive_species_detection\postgres":/var/lib/postgresql/data -d postgis/postgis
```