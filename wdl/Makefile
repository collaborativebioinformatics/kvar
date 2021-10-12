
PROJECT_ID=project-G5Q6BVQ0jgqvP3Qk1yG5q8Bg
FOLDER=/wdl/tasks
WORKFLOW_FOLDER=/wdl/workflow

download-jar:
	wget https://github.com/dnanexus/dxWDL/releases/download/v1.50/dxWDL-v1.50.jar

compile-tasks:
	java -jar dxWDL-v1.50.jar compile ./tasks.wdl -project $(PROJECT_ID) -folder $(FOLDER)

compile-workflow:
	java -jar dxWDL-v1.50.jar compile ./workflow.wdl -project $(PROJECT_ID) -folder $(WORKFLOW_FOLDER)