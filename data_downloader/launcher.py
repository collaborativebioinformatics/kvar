import argparse
import logging
from typing import List, Dict

from dxpy.bindings.dxapp import DXApp
from dxpy.bindings.dxjob import DXJob


SRA_APP_NAME = "sra_fastq_importer"


def parse_sra_file(sra_file: str) -> List[str]:
    """Parse sra file and return a list of SRA

    Args:
        sra_file: name of sra file. contains one srr accession id per line

    Returns:
        List of sra accession
    """
    sra_ids = []
    with open(sra_file) as fh_in:
        for line in fh_in:
            line = line.strip()
            if line:
                sra_ids.append(line.strip())
    return sra_ids


def sra_id_to_app_input(sra_id: str) -> Dict:
    """Generate input from app for sra_fastq_importer

    Set split files to false so we no merging is needed

    Args:
        sra_id:

    Returns:
        dictionary containing
    """
    return {"accession": sra_id, "split_files": False}


def launch_jobs_for_sra_ids(
    sra_import_app: DXApp, sra_ids: List[str], folder
) -> Dict[str, DXJob]:
    """Launch sra_import_app on a list of sra_ids

    Args:
        sra_import_app: app instance
        sra_ids: list of SRA ids
        folder: output folder on dnanexus

    Returns:
        jobs: where key is sra id and the value is the dx job instance.

    """
    jobs = {}

    for sra_id in sra_ids:
        dx_job = sra_import_app.run(
            sra_id_to_app_input(sra_id),
            name=f"{sra_id}-import",
            folder=folder,
            instance_type="mem1_ssd2_v2_x36",
        )
        jobs[sra_id] = dx_job

    return jobs


def log_job_infos(sra_to_job_objs: Dict[str, DXJob], job_log: str) -> None:
    """Generate txt contain sra to job id info

    Args:
        sra_to_job_objs: dictionary where key is the sra id and the value is the dx job instance
        job_log: output log file

    """
    with open(job_log, "w") as fh_out:
        for sra, job_obj in sra_to_job_objs.items():
            job_id = job_obj.get_id()
            fh_out.write(f"{sra}\t{job_id}\n")


def main(sra_file: str, output_folder: str, job_log: str) -> None:
    """Runs SRA on a list of file

    Args:
        sra_file: sra file
        output_folder: location on dnanexus where the files will be found
        job_log: log file containing sra to job id

    """
    app = DXApp(name="sra_fastq_importer")
    logging.info(f"Parsing SRA file: {sra_file}")
    sra_ids = parse_sra_file(sra_file)
    logging.info(f"Launching {len(sra_file)} jobs.")
    sra_to_job_obj = launch_jobs_for_sra_ids(app, sra_ids, output_folder)
    logging.info(f"Launched {len(sra_file)} jobs.")

    log_job_infos(sra_to_job_obj, job_log)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--accession-file",
        "-i",
        help="txt file containing SRR file, one per line.",
        required=True,
    )
    parser.add_argument(
        "--dx-folder",
        "-f",
        help="destination of output file on dnanexus platform",
        required=True,
    )
    parser.add_argument(
        "--log-file",
        "-o",
        help="log file",
        required=True,
    )
    args = parser.parse_args()
    main(args.accession_file, args.dx_folder, args.log_file)
