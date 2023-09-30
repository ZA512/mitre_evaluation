import os
import json
import argparse

parser = argparse.ArgumentParser(description="Script pour traiter les fichiers JSON dans le dossier d'évaluation.")
parser.add_argument("annee", help="Nom du sous-dossier (l'année) à traiter")
args = parser.parse_args()

dossier_evaluation = os.path.join("evaluation", args.annee)

ordre_preference = ["Technique", "Tactic", "General", "Telemetry", "None", "N/A"]
colonnes = ["Nom du fichier JSON","blocked"]
colonnes.extend([f"{elem} totale" for elem in ordre_preference])
colonnes.extend([f"{elem} modifier" for elem in ordre_preference])
colonnes.extend([f"{elem} step sans modifier" for elem in ordre_preference])
colonnes.extend([f"{elem} step avec modifier" for elem in ordre_preference])

valeurs_par_colonne = {colonne: [] for colonne in colonnes}

for fichier_json in os.listdir(dossier_evaluation):
	if fichier_json.endswith(".json"):
		chemin_fichier = os.path.join(dossier_evaluation, fichier_json)
		
		with open(chemin_fichier, 'r') as fichier:
			donnees_json = json.load(fichier)

			nom_fichier = fichier_json
			compteur_par_type = {elem: {"total": 0, "modifier": 0, "step_sans_modifier": 0, "step_avec_modifier": 0} for elem in ordre_preference}
			blocked_count = 0
			test_num_count = 0
			step_count = 0
			adversaires = donnees_json.get("Adversaries", [])
			
			for adversaire in adversaires:
				for step_name, step_data in adversaire.get("Detections_By_Step", {}).items():
					for step in step_data.get("Steps", []):
						for substep in step.get("Substeps", []):
							technique_for_this_step = 0
							tactic_for_this_step = 0
							general_for_this_step = 0
							telemetry_for_this_step = 0
							none_for_this_step = 0
							na_for_this_step = 0							
							technique_for_this_step_mod = 0
							tactic_for_this_step_mod = 0
							general_for_this_step_mod = 0
							telemetry_for_this_step_mod = 0
							none_for_this_step_mod = 0
							na_for_this_step_mod = 0
							step_count += 1
							for detect in substep.get("Detections", []):
								detection_type = detect.get("Detection_Type")
								modifiers = detect.get("Modifiers")
								
								if detection_type in ordre_preference:
									compteur_par_type[detection_type]["total"] += 1
									if modifiers:
										compteur_par_type[detection_type]["modifier"] += 1

								if detection_type == "Technique":
									if modifiers:
										technique_for_this_step_mod = 1
									else:
										technique_for_this_step = 1
								if detection_type == "Tactic":
									if modifiers:
										tactic_for_this_step_mod = 1
									else:
										tactic_for_this_step = 1
								if detection_type == "General":
									if modifiers:
										general_for_this_step_mod = 1
									else:
										general_for_this_step = 1
								if detection_type == "Telemetry":
									if modifiers:
										telemetry_for_this_step_mod = 1
									else:
										telemetry_for_this_step = 1	
								if detection_type == "None":
									if modifiers:
										none_for_this_step_mod = 1
									else:
										none_for_this_step = 1	
								if detection_type == "N/A":
									if modifiers:
										na_for_this_step_mod = 1
									else:
										na_for_this_step = 1
										
							if technique_for_this_step_mod == 1:
								compteur_par_type["Technique"]["step_avec_modifier"] += 1
							elif tactic_for_this_step_mod == 1:
								compteur_par_type["Tactic"]["step_avec_modifier"] += 1
							elif general_for_this_step_mod == 1:
								compteur_par_type["General"]["step_avec_modifier"] += 1
							elif telemetry_for_this_step_mod == 1:
								compteur_par_type["Telemetry"]["step_avec_modifier"] += 1
							elif none_for_this_step_mod == 1:
								compteur_par_type["None"]["step_avec_modifier"] += 1
							elif na_for_this_step_mod == 1:
								compteur_par_type["N/A"]["step_avec_modifier"] += 1
							
							if technique_for_this_step == 1:
								compteur_par_type["Technique"]["step_sans_modifier"] += 1
							elif tactic_for_this_step == 1:
								compteur_par_type["Tactic"]["step_sans_modifier"] += 1
							elif general_for_this_step == 1:
								compteur_par_type["General"]["step_sans_modifier"] += 1
							elif telemetry_for_this_step == 1:
								compteur_par_type["Telemetry"]["step_sans_modifier"] += 1
							elif none_for_this_step == 1:
								compteur_par_type["None"]["step_sans_modifier"] += 1
							elif na_for_this_step == 1:
								compteur_par_type["N/A"]["step_sans_modifier"] += 1
								
				for step_name, step_data in adversaire.get("Protections", {}).items():
					for item in step_data:
						substeps = item.get('Substeps', [])
						for substep in substeps:
							if substep.get("Protection_Type") == "Blocked":
								blocked_count += 1
						test_nums = item.get('Test_Num', [])
						test_num_count = test_nums
				
			valeurs_par_colonne["Nom du fichier JSON"].append(nom_fichier)
			valeurs_par_colonne["blocked"].append(blocked_count)
			for elem in ordre_preference:
				total = compteur_par_type[elem]["total"]
				modifier = compteur_par_type[elem]["modifier"]
				step_sans_modifier = compteur_par_type[elem]["step_sans_modifier"]
				step_avec_modifier = compteur_par_type[elem]["step_avec_modifier"]
				valeurs_par_colonne[f"{elem} totale"].append(total)
				valeurs_par_colonne[f"{elem} modifier"].append(modifier)
				valeurs_par_colonne[f"{elem} step sans modifier"].append(step_sans_modifier)
				valeurs_par_colonne[f"{elem} step avec modifier"].append(step_avec_modifier)
				
html_table = "<!DOCTYPE html>"
html_table += "<html lang=\"fr\">"
html_table += "<head>"
html_table += "    <meta charset=\"UTF-8\">"
html_table += "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
html_table += "    <title>Titre de la page</title>"
html_table += "<link href=\"https://unpkg.com/tabulator-tables@5.5.2/dist/css/tabulator.min.css\" rel=\"stylesheet\">"
html_table += "<script type=\"text/javascript\" src=\"https://unpkg.com/tabulator-tables@5.5.2/dist/js/tabulator.min.js\"></script>"
html_table += "</head><body>"

html_table += "<table  id='mitre'>\n<thead><tr>"
html_table += "<th>Nom du fichier JSON</th>"
html_table += "<th>Blocked / "+ str(test_num_count) +"</th>"
html_table += "<th>TECHNIQUE all</th>"
html_table += "<th>TECHNIQUE all modifier</th>"
html_table += "<th>TECHNIQUE in step / "+ str(step_count) +"</th>"
html_table += "<th>TECHNIQUE in step modifier</th>"
html_table += "<th>TACTIC all</th>"
html_table += "<th>TACTIC all modifier</th>"
html_table += "<th>TACTIC in step</th>"
html_table += "<th>TACTIC in step modifier</th>"
html_table += "<th>GENERAL all</th>"
html_table += "<th>GENERAL all modifier</th>"
html_table += "<th>GENERAL in step</th>"
html_table += "<th>GENERAL in step modifier</th>"
html_table += "<th>TELEMETRY all</th>"
html_table += "<th>TELEMETRY all modifier</th>"
html_table += "<th>TELEMETRY in step</th>"
html_table += "<th>TELEMETRY in step modifier</th>"
html_table += "<th>NONE all</th>"
html_table += "<th>NONE all modifier</th>"
html_table += "<th>NONE in step</th>"
html_table += "<th>NONE in step modifier</th>"
html_table += "<th>N/A all</th>"
html_table += "<th>N/A all modifier</th>"
html_table += "<th>N/A in step</th>"
html_table += "<th>N/A in step modifier</th>"
html_table += "</tr></thead>\n"

html_table += "<tbody>"
for i in range(len(valeurs_par_colonne["Nom du fichier JSON"])):
	html_table += "<tr>"
	html_table += f"<td>{valeurs_par_colonne['Nom du fichier JSON'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['blocked'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['Technique totale'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['Technique modifier'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['Technique step sans modifier'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['Technique step avec modifier'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['Tactic totale'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['Tactic modifier'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['Tactic step sans modifier'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['Tactic step avec modifier'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['General totale'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['General modifier'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['General step sans modifier'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['General step avec modifier'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['Telemetry totale'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['Telemetry modifier'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['Telemetry step sans modifier'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['Telemetry step avec modifier'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['None totale'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['None modifier'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['None step sans modifier'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['None step avec modifier'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['N/A totale'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['N/A modifier'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['N/A step sans modifier'][i]}</td>"
	html_table += f"<td>{valeurs_par_colonne['N/A step avec modifier'][i]}</td>"
	html_table += "</tr>\n"

html_table += "</tbody></table>"	
html_table += "all =  counts all detections. Sometimes there can be several detections within a single step.<br>" 
html_table += "all modifier =  count each detection obtained by changing the default configuration<br>"
html_table += "in step =  in each step, only the highest detection type is counted, but without changing the default configuration<br>"
html_table += "in step =  in each step only the highest detection type is counted, but obtained by changing the default configuration<br>"
html_table += "<script>"
html_table += "	var table = new Tabulator(\"#mitre\", {});"
html_table += "</script></body></html>"

with open("Mitre Evaluation " + str(args.annee) + ".html", 'w') as fichier_html:
	fichier_html.write(html_table)