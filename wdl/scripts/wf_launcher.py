import argparse
import json
import os
from collections import defaultdict
from typing import Dict

import dxpy


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--workflow_id", help="workflow id", default="workflow-G5XJz6Q0jgqq5VYfJP4Y6z3g"
    )
    parser.add_argument(
        "--input_folder", help="input folder containing sra files", required=True
    )
    parser.add_argument(
        "--output_folder",
        help="output folder containing trimmed reads and jellyfish count",
        required=True,
    )
    parser.add_argument("--kmer_size", default=21, type=int)
    parser.add_argument("--out_log", help="write log files")
    return parser.parse_args()


def parse_dx_input_folder(dx_folder: str) -> Dict[str, str]:

    name_to_file_id = {}
    dx_objects = dxpy.bindings.dxproject.DXProject().list_folder(
        dx_folder, describe=True
    )["objects"]

    for dx_object in dx_objects:
        dx_name = dx_object["describe"]["name"]
        dx_id = dx_object["id"]

        name_to_file_id[dx_name] = dx_id
    return name_to_file_id


def group_file_name_into_pairs(
    name_to_file_id: Dict[str, str]
) -> Dict[str, Dict[str, str]]:
    grouped = defaultdict(dict)
    for dx_name, dx_id in name_to_file_id.items():
        sample_name = dx_name.split("_")[0]
        read_number = "r1"
        if "_2.fastq.gz" in dx_name:
            read_number = "r2"

        grouped[sample_name][read_number] = dx_id

    return grouped


def launch_workflow(
    grouped_fastqs: Dict[str, Dict[str, str]],
    output_folder: str,
    workflow_id: str,
    kmer_size: int,
) -> Dict[str, Dict[str, Dict[str, str]]]:

    job_id_details = {}

    dx_workflow = dxpy.DXWorkflow(workflow_id)
    for sample_name, read_inputs in grouped_fastqs.items():
        wf_input = {
            "stage-common.kmer_size": kmer_size,
            "stage-common.in_fastq_r1": {"$dnanexus_link": read_inputs["r1"]},
            "stage-common.in_fastq_r2": {"$dnanexus_link": read_inputs["r2"]},
        }
        out_path = os.path.join(output_folder, sample_name)
        print(f"starting {sample_name}. output at {out_path}")
        dx_run = dx_workflow.run(wf_input, folder=out_path)
        job_id = dx_run.get_id()

        job_id_details[job_id] = {sample_name: read_inputs, "out_path": out_path}
    return job_id_details


def write_log(job_id_details, output):
    with open(output, "w") as f:
        json.dump(job_id_details, f, indent=2)


def main(workflow_id, output_folder, input_folder, kmer_size, out_log):
    name_to_file_id = parse_dx_input_folder(input_folder)
    grouped_samples = group_file_name_into_pairs(name_to_file_id)
    job_id_details = launch_workflow(
        grouped_samples, output_folder, workflow_id, kmer_size
    )
    write_log(job_id_details, out_log)


if __name__ == "__main__":
    args = parse_args()
    main(
        args.workflow_id,
        args.output_folder,
        args.input_folder,
        args.kmer_size,
        args.out_log,
    )
