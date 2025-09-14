# Interactivity

- Streamlit demo app: quick GUI exploration with PN and LED tabs.
- ipywidgets notebooks: fine-grained, in-notebook sliders for parameters.

## Streamlit App

Run locally from the repo root:

```powershell
python -m streamlit run examples/app_interactive.py
```

If using workspace tasks, ensure the venv has `streamlit` installed
(see `requirements.txt`).

### What’s Inside

- PN tab: sliders for dopings, area, temperature, voltage range; plots current
  and SRH recombination.
- LED tab: sliders for dopings, efficiency, temperature, voltage; plots current,
  emission, and recombination.

## Notebooks

Open the interactive examples in Jupyter:

```powershell
jupyter notebook examples/example_led_interactive.ipynb
jupyter notebook examples/example_pn_interactive.ipynb
```

Requirements: `ipywidgets`, `plotly`. Use the provided sliders to update plots.

## Tips

- For headless environments, plotting uses Plotly in the app and widgets in
  notebooks.
- If ports are blocked, Streamlit prints a local URL you can open manually.
