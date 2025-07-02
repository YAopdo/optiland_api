from flask import Flask, request, send_file, jsonify
import numpy as np
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from optiland import optic
import tempfile
import os

app = Flask(__name__)

@app.route('/simulate', methods=['POST'])
def simulate_lens():
    try:
        surfaces = request.json

        lens = optic.Optic()
        lens.add_surface(index=0, thickness=np.inf)

        for i, surf in enumerate(surfaces, start=1):
            kwargs = {
                "index": i,
                "radius": surf["radius"],
                "thickness": surf["thickness"]
            }
            if "material" in surf:
                kwargs["material"] = surf["material"]
            if "surface_type" in surf:
                kwargs["surface_type"] = surf["surface_type"]
            if "conic" in surf:
                kwargs["conic"] = surf["conic"]
            if "coefficients" in surf:
                kwargs["coefficients"] = surf["coefficients"]

            lens.add_surface(**kwargs)

        lens.add_surface(index=len(surfaces)+1, is_stop=True)
        lens.set_aperture(aperture_type="EPD", value=10)
        lens.set_field_type(field_type="angle")
        lens.add_field(y=0)
        lens.add_wavelength(value=0.48)

        lens.draw(num_rays=10)
        plt.xlabel("")
        plt.ylabel("")
        plt.title("")
        plt.xticks([])
        plt.yticks([])

        temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        plt.savefig(temp_file.name, dpi=300)
        plt.close()

        return send_file(temp_file.name, mimetype='image/png')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
