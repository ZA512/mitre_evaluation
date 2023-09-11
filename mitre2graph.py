import os
import json
import argparse
import numpy as np
import matplotlib.pyplot as plt

def create_json_graph(json_filename):
	with open(json_filename, "r") as json_file:
		json_data = json_file.read()

	data = json.loads(json_data)
	adversaries = data["Adversaries"]
	substeps_list = []
	detection_types = ["Technique", "Tactic", "General", "Telemetry", "None", "N/A"]

	def modify_modifiers(modifiers):
		modified_modifiers = []
		for modifier in modifiers:
			if "UX Change" in modifier:
				modified_modifiers.append("UX Change")
			if "Detection Logic" in modifier:
				modified_modifiers.append("Detection Logic")
			if "Data Source" in modifier:
				modified_modifiers.append("Data Source")
		return modified_modifiers

	num_detection_types = len(detection_types)

	for adversary in adversaries:
		detections_by_step = adversary["Detections_By_Step"]

		for scenario_data in detections_by_step.values():
			steps = scenario_data["Steps"]

			for step in steps:
				for substep in step.get("Substeps", []):
					substep_value = substep.get("Substep", "N/A")
					if substep_value not in substeps_list:
						substeps_list.append(substep_value)

	num_substeps = len(substeps_list)
	data_matrix = np.zeros((num_detection_types, num_substeps))

	modifiers_for_detection = [[False] * num_substeps for _ in range(num_detection_types)]
	modifiers_text = [[False] * num_substeps for _ in range(num_detection_types)]

	for adversary in adversaries:
		detections_by_step = adversary["Detections_By_Step"]

		for scenario_data in detections_by_step.values():
			steps = scenario_data["Steps"]

			for step in steps:
				for substep in step.get("Substeps", []):
					substep_value = substep.get("Substep", "N/A")

					for detection in substep.get("Detections", []):
						detection_type = detection.get("Detection_Type", "N/A")
						modifiers = modify_modifiers(detection.get("Modifiers", []))

						row_idx = detection_types.index(detection_type)
						col_idx = substeps_list.index(substep_value)
						data_matrix[row_idx, col_idx] += 1

						if modifiers:
							modifiers_for_detection[row_idx][col_idx] = True
							modifiers_text[row_idx][col_idx] = modifiers

	plt.figure(figsize=(10, 6))
	cmap = plt.get_cmap("YlOrRd")
	plt.imshow(data_matrix, cmap=cmap, aspect="auto", vmin=0, vmax=data_matrix.max() + 1)

	for i in range(num_detection_types):
		for j in range(num_substeps):
			if data_matrix[i, j] > 0:
				if i == 0:
					if modifiers_for_detection[i][j]:
						plt.gca().add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, edgecolor='black', facecolor='#95bd2a'))
						varmodifier = ""
						if "UX Change" in modifiers_text[i][j]:
							varmodifier += "U\nX\n"
						if "Detection Logic" in modifiers_text[i][j]:
							if varmodifier:
								varmodifier += "+\n"
							varmodifier += "D\nL\n"
						if "Data Source" in modifiers_text[i][j]:
							if varmodifier:
								varmodifier += "+\n"
							varmodifier += "D\nS\n"

						plt.text(j, i, varmodifier, ha='center', va='center', color='black')
					else:
						plt.gca().add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, edgecolor='black', facecolor='#95bd2a'))
				if i == 1:
					if modifiers_for_detection[i][j]:
						plt.gca().add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, edgecolor='black', facecolor='#05ae6a'))
						varmodifier = ""
						if "UX Change" in modifiers_text[i][j]:
							varmodifier += "U\nX\n"
						if "Detection Logic" in modifiers_text[i][j]:
							if varmodifier:
								varmodifier += "+\n"
							varmodifier += "D\nL\n"
						if "Data Source" in modifiers_text[i][j]:
							if varmodifier:
								varmodifier += "+\n"
							varmodifier += "D\nS\n"
						plt.text(j, i, varmodifier, ha='center', va='center', color='black')
					else:
						plt.gca().add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, edgecolor='black', facecolor='#05ae6a'))
				if i == 2:
					if modifiers_for_detection[i][j]:
						plt.gca().add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, edgecolor='black', facecolor='#00978d'))
						varmodifier = ""
						if "UX Change" in modifiers_text[i][j]:
							varmodifier += "U\nX\n"
						if "Detection Logic" in modifiers_text[i][j]:
							if varmodifier:
								varmodifier += "+\n"
							varmodifier += "D\nL\n"
						if "Data Source" in modifiers_text[i][j]:
							if varmodifier:
								varmodifier += "+\n"
							varmodifier += "D\nS\n"
						plt.text(j, i, varmodifier, ha='center', va='center', color='black')
					else:
						plt.gca().add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, edgecolor='black', facecolor='#00978d'))
				if i == 3:
					if modifiers_for_detection[i][j]:
						plt.gca().add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, edgecolor='black', facecolor='#ffbb05'))
						varmodifier = ""
						if "UX Change" in modifiers_text[i][j]:
							varmodifier += "U\nX\n"
						if "Detection Logic" in modifiers_text[i][j]:
							if varmodifier:
								varmodifier += "+\n"
							varmodifier += "D\nL\n"
						if "Data Source" in modifiers_text[i][j]:
							if varmodifier:
								varmodifier += "+\n"
							varmodifier += "D\nS\n"
						plt.text(j, i, varmodifier, ha='center', va='center', color='black')
					else:
						plt.gca().add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, edgecolor='black', facecolor='#ffbb05'))
				if i == 4:
					if modifiers_for_detection[i][j]:
						plt.gca().add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, edgecolor='black', facecolor='#007a9a'))
						varmodifier = ""
						if "UX Change" in modifiers_text[i][j]:
							varmodifier += "U\nX\n"
						if "Detection Logic" in modifiers_text[i][j]:
							if varmodifier:
								varmodifier += "+\n"
							varmodifier += "D\nL\n"
						if "Data Source" in modifiers_text[i][j]:
							if varmodifier:
								varmodifier += "+\n"
							varmodifier += "D\nS\n"
						plt.text(j, i, varmodifier, ha='center', va='center', color='black')
					else:
						plt.gca().add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, edgecolor='black', facecolor='#007a9a'))
				if i == 5:
					if modifiers_for_detection[i][j]:
						plt.gca().add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, edgecolor='black', facecolor='#185b85'))
						varmodifier = ""
						if "UX Change" in modifiers_text[i][j]:
							varmodifier += "U\nX\n"
						if "Detection Logic" in modifiers_text[i][j]:
							if varmodifier:
								varmodifier += "+\n"
							varmodifier += "D\nL\n"
						if "Data Source" in modifiers_text[i][j]:
							if varmodifier:
								varmodifier += "+\n"
							varmodifier += "D\nS\n"
						plt.text(j, i, varmodifier, ha='center', va='center', color='black')
					else:
						plt.gca().add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, edgecolor='black', facecolor='#185b85'))


	plt.yticks(range(num_detection_types), detection_types)
	plt.xticks(range(num_substeps), substeps_list, rotation=90)

	plt.ylabel("Detection_Type")
	plt.xlabel("Substep")
	filename_without_extension = os.path.splitext(os.path.basename(json_filename))[0]
	plt.title(f" {filename_without_extension}")

parser = argparse.ArgumentParser(description="Script pour traiter les fichiers JSON dans le dossier d'évaluation.")
parser.add_argument("annee", help="Nom du sous-dossier (l'année) à traiter")
args = parser.parse_args()

evaluation_folder = os.path.join("evaluation", args.annee)
json_files = [os.path.join(evaluation_folder, file) for file in os.listdir(evaluation_folder) if file.endswith(".json")]

for json_filename in json_files:
	create_json_graph(json_filename)

plt.show()