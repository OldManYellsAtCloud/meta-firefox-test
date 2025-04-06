from pathlib import Path
from pybadges import badge
import requests
import json
import time
import argparse

def parse_job_name(job_name):
    # It looks like "test (walnascar, latest, musl, x86-64)"
    # Extract all tokens
    job_type = job_name.split()[0]
    yocto_version = job_name.split("(")[1].split(",")[0]
    ff_version = job_name.split()[2][:-1]
    libc_flavour = job_name.split()[3][:-1]
    arch = job_name.split()[4][:-1]
    return job_type, yocto_version, ff_version, libc_flavour, arch


def generate_badge(job, yocto, libc, arch, status, destination):
    if status == "success":
        right_color = "brightgreen"
    elif status == "failure":
        right_color = "red"
    else:
        right_color = "lightgrey"

    file_name = "%s-%s-%s-%s.svg" % (job, yocto, libc, arch)
    file_path = destination + "/" + file_name
    b = badge(left_text=job, right_text=status, left_color="grey", right_color=right_color)
    with open(file_path, "w") as file:
        file.write(b)


def query_results(job_id, save_dest, esr_version, latest_version):
    base_url = "https://api.github.com/repos/OldManYellsAtCloud/meta-browser/actions/runs/{}/jobs".format(job_id)

    query_next = True
    all_success = True

    while query_next:
        response = requests.get(url=base_url)
        for job in response.json()["jobs"]:
            job_name = job["name"]
            if "Test Results" in job_name:
                 continue

            conclusion = job["conclusion"]
            job_type, yocto_version, ff_version, libc_flavour, arch = parse_job_name(job_name)

            if esr_version is None and ff_version == "esr":
                continue
            if latest_version is None and ff_version == "latest":
                continue

            if ff_version == "esr":
                destination = save_dest + esr_version
            else:
                destination = save_dest + latest_version

            if not conclusion == "success":
                all_success = False

            generate_badge(job_type, yocto_version, libc_flavour, arch, conclusion, destination)

        if 'rel="next"' in response.headers["Link"]:
            links = response.headers["Link"].split(",")
            for link in links:
                if 'rel="next"' in link:
                    base_url = link.split("<")[1].split(">")[0]
                    time.sleep(3)
                    break
        else:
            query_next = False

    return all_success


def query_loop(job_id, save_dest, esr_version, latest_version):
    loop_sleep_sec = 2700
    while not query_results(job_id, save_dest, esr_version, skip_esr, latest_version, skip_latest):
        time.sleep(loop_sleep_sec)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--run_id', required=True)
  parser.add_argument('--esr_version')
  parser.add_argument('--latest_version')
  parser.add_argument('--icon_folder', required=True)
  args = parser.parse_args()

  if not args.icon_folder.endswith('/'):
      args.icon_folder += '/'

  if esr_version:
      Path(args.icon_folder + esr_version).mkdir(parents=True, exist_ok=True)

  if latest_version:
      Path(args.icon_folder + latest_version).mkdir(parents=True, exist_ok=True)

  if not latest_version and not esr_version:
      print("No latest_version nor esr_version present? What's the plan exactly?')
      exit(1)
      
  query_loop(args.run_id, args.icon_folder, args.esr_version, args.latest_version)
   
