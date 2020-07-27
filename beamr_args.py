#!/usr/bin/env python
import argparse
import os, sys
import re
import json
from urllib.parse import urlparse
import logging

# need  jsonpath-rw from git (https://github.com/kennknowles/python-jsonpath-rw)
# then install jsonpath-rw-ext: pip install jsonpath-rw-ext
import jsonpath_rw_ext 


def main():

	# process args
	parser = argparse.ArgumentParser(description='Convert a beamr .cfg file into a Hybrik Job')
	parser.add_argument('-c', '--config', type=argparse.FileType('r'), help='beamr.cfg file)', required=True)
	parser.add_argument('--verbose', action='store_true', help="Verbose output", default=False)

	parser.add_argument('job', type=argparse.FileType('r'), help="input job file")

	# parse args
	args = parser.parse_args()

	# setup logging, run -v for output
	if args.verbose:
	    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
	    logging.info("Verbose output.")
	else:
	    logging.basicConfig(format="%(levelname)s: %(message)s")

	# Get source json
	# ensure we have valid json input
	try:
		source_hybrik_job = json.load(args.job)
	except json.decoder.JSONDecodeError as e:
		logging.error("Invalid json supplied in Hybrik job")
	except Exception:
		raise

	# debug output
	logging.debug(json.dumps(source_hybrik_job, indent=4))


	### process beamr cfg file
	compiled_beamr_args = ""
	for line in args.config:
		
		# don't log any newlines from the config file
		logging.info("config line: " + re.sub("\n", "", str(line)))

		# try to match for a config line we want to keep, strip white space, newlines, tabs, etc.  Ignore commments.
		try:
			result = re.sub("\s", "", re.search("^(?!\#|input|\/\/)(.[^\/]+|.+)", line).group(0)) + " "
		except AttributeError as e:
			logging.info("line we don't want: " + str(line))
			continue

		compiled_beamr_args += result

	# strip final space
	compiled_beamr_args = compiled_beamr_args.rstrip()
	
	## Create or append to definitions
	# remember sources for definitions
	if "definitions" not in source_hybrik_job.keys():
		# this uglyness to put the definitoins key at the top
		logging.info("Input job does not have definitions, adding...")
		temp_dict = {}
		temp_dict["definitions"] = {
			"beamr4x_options": compiled_beamr_args
		}

		temp_dict.update(source_hybrik_job)
		source_hybrik_job = temp_dict
	else:
		logging.info("Input job contains definitions, adding beamr: " + str(line))
		source_hybrik_job["definitions"]["beamr4x_options"] = compiled_beamr_args


	## Update each video target that uses beamr4x
	items = jsonpath_rw_ext.parse('$..targets[?(video.codec_provider = "beamr4x")].video').find(source_hybrik_job)
	for item in items:

		# copy the inmutable object
		item_copy = item.value
		logging.info("target before update" + json.dumps(item_copy, indent = 4))

		# insert the placeholder
		item_copy["beamr4x_options"] = "{{beamr4x_options}}"
		pattern = jsonpath_rw_ext.parse(str(item.full_path))
		json_object = pattern.update(source_hybrik_job, item_copy)


	## Write output new job
	beamr_job_file = str(args.job.name.split(".")[0] + "_updated.json")
	logging.info("Saving the json job to a file: " + beamr_job_file)
	try:
		with open(beamr_job_file, 'w') as f:
			f.write(json.dumps(source_hybrik_job, indent = 4))
	except Exception as e:
		logging.error("Could not write updated file")

	print("Updated job created: " + beamr_job_file)





# main
if __name__ == "__main__":
    main()





