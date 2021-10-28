from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from random import sample
import requests
import pandas as pd


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


github_packages = {
    "py": [
        "networkx/networkx",
        "numpy/numpy",
        "scipy/scipy",
        "scikit-learn/scikit-learn",
        "pandas-dev/pandas",
        "scikit-image/scikit-image",
    ]
}

langs = ["py"]


@app.get("/{extension}")
def generate_random_file(extension: str):
    if extension not in langs:
        raise HTTPException(
            status_code=404, detail="Currently we also support python files."
        )
    random_package = sample(github_packages[extension], 1)[0]
    API_URL = (
        f"https://api.github.com/repos/{random_package}/git/trees/HEAD?recursive=1"
    )
    github_response = requests.get(API_URL)
    print(API_URL)
    files = pd.DataFrame(github_response.json()["tree"])
    file_path = files[files.path.str.endswith(".py")].sample(1).path.values[0]

    return RedirectResponse(
        f"https://github.dev/{random_package}/blob/HEAD/{file_path}"
    )
