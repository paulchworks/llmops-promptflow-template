# How to setup the repo with Jenkins

This is a guide to set up the repository with Jenkins Pipelines for experimenting and evaluating Prompt flows in Azure Machine Learning. The repository contains examples of Prompt flow runs and evaluations for named entity recognition, math coding, and web classification. 

This template supports Azure Machine Learning (ML) as a platform for LLMOps, and Jenkins Pipelines as a platform for Flow operationalization. LLMOps with Prompt flow provides automation of:

* Experimentation by executing flows
* Evaluation of prompts along with their variants  
* Registration of prompt flow 'flows'
* Deployment of prompt flow 'flows'
* Generation of Docker Image
* Deployment to Kubernetes, Azure Web Apps and Azure ML compute
* A/B deployments
* Role based access control (RBAC) permissions to deployment system managed id to key vault and Azure ML workspace
* Endpoint testing
* Report generation

It is important to understand how [Prompt flow works](https://learn.microsoft.com/en-us/azure/machine-learning/prompt-flow/get-started-prompt-flow?view=azureml-api-2) before using this template.

## Prerequisites

- An Azure subscription. If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version of Machine Learning](https://azure.microsoft.com/free/).
- An Azure Machine Learning workspace.
- Git running on your local machine.
- GitHub as the source control repository.
- Azure OpenAI with Model deployed with name `gpt-35-turbo`.
- In case of Kubernetes based deployment, Kubernetes resources and associating it with Azure Machine Learning workspace would be required. More details about using Kubernetes as compute in AzureML is available [here](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-attach-kubernetes-anywhere?view=azureml-api-2).

The template deploys real-time online endpoints for flows. These endpoints have Managed ID assigned to them and in many cases they need access to Azure Machine learning workspace and its associated key vault. The template by default provides access to both the key vault and Azure Machine Learning workspace based on this [document](https://learn.microsoft.com/en-ca/azure/machine-learning/prompt-flow/how-to-deploy-for-real-time-inference?view=azureml-api-2#grant-permissions-to-the-endpoint).

## Execution

This section provides instructions on how to execute template either locally or on Azure, based on the configuration specified in the `config.py` file within the `llmops` folder.

### config.py

The `config.py` file located in the `llmops` folder contains the `EXECUTION_TYPE` variable, which determines where the flow will be executed.

- Set `EXECUTION_TYPE = "LOCAL"` to execute the flows on your local machine.
- Set `EXECUTION_TYPE = "AZURE"` to execute the flows on Azure.

### Local Execution

When the `EXECUTION_TYPE` variable is set to `"LOCAL"`, the templates will be executed on your local machine. This is useful for local development, testing, and debugging.

To execute a template locally, use the following command:

Setup the environment by installing the required dependencies using the following command:

``` bash
pip install -r ./github/requirements/execute_job_requirements.txt

# select the requirements file based on the usecase you are working on e.g. for web_classification
pip install -r ./web_classification/flows/experiment/requirements.txt

```

``` bash
python -m llmops.common.prompt_pipeline --base_path ./<example_path> --variants <template_name>
```

Replace `<example_path>` with the path to the specific example you want to run (e.g., `./web_classification`) and `<template_name>` with the name of the template (e.g., `summarize_text_content.variant_0`). The `--variants` argument is optional and can be used to specify the variant of the template to run.

Ensure that you have a .env file with valid values for the required environment variables. The .env file should be located in the root directory of the example you are running. An example .env.sample file is provided which can be renamed to .env file.

### Azure Execution

When the `EXECUTION_TYPE` variable is set to `"AZURE"`, the flows will be executed on Azure. This allows you to leverage the scalability and resources provided by Azure for running your experiments and evaluations.

There are two ways to execute templates on Azure:

1. **CI/CD Pipelines**: Set up a CI/CD pipeline in your Azure DevOps/Github/Jenkins. Configure the pipeline to trigger the execution of the template on Azure. Ensure that the `EXECUTION_TYPE` variable in `config.py` is set to `"AZURE"`.

2. **Direct Execution from Local Machine**: You can also execute templates on Azure directly from your local machine. Set the `EXECUTION_TYPE` variable in `config.py` to `"AZURE"` and use the following command:

Setup the environment by installing the required dependencies using the following command:

``` bash
pip install -r ./github/requirements/execute_job_requirements.txt

# select the requirements file based on the usecase you are working on e.g. for web_classification
pip install -r ./web_classification/flows/experiment/requirements.txt

```

``` bash
python -m llmops.common.prompt_pipeline --base_path ./<example_path> --variants <template_name>
```

Ensure that you have a .env file with valid values for the required environment variables. The .env file should be located in the root directory of the example you are running. An example .env.sample file is provided which can be renamed to .env file.


### Important Considerations

- Make sure to review and modify the `config.py` file based on your specific requirements and environment setup.
- Ensure that you have the necessary dependencies installed and the required configurations set up for the execution environment you choose LOCAL.
- When executing templates on Azure, ensure that you have the appropriate permissions and credentials set up to access Azure resources.
- Be aware of any costs associated with running experiments and evaluations on Azure, as it may incur charges based on resource usage.

## Secrets Management

This template utilizes secrets to securely store sensitive information such as API keys, credentials, and other confidential data. Secrets are managed differently depending on the execution environment, whether it's local execution or execution through Jenkins pipelines.

### Local Execution

For local execution, secrets are stored in a .env file located in the template's root directory. The .env file contains key-value pairs representing the secrets. For example:

``` bash
AOAI_API_KEY=abcdefghijklmnop
max_total_token=4096
```
The .env file is already added to the .gitignore file to prevent it from being committed and pushed to the remote repository, keeping the secrets secure.

### Jenkins Secrets

When executing the template through Jenkins pipelines, secrets are stored within Jenkins environment. In this template, a secret named 'ENV_VARS' is used to store the secrets. The 'ENV_VARS' secret should contain the same key-value pairs as the .env file. For example:

``` bash
AOAI_API_KEY=abcdefghijklmnop
AZURE_OPENAI_API_KEY=xxxxxx
```

Jenkins secrets can be accessed and managed within Jenkins by navigating to Secret Credentials tab within Manage Jenkins dashboard.

### Referencing Secrets
Secrets are referenced in the experiment.yaml, flex.flow.yaml, init.json and env.yaml files using a special syntax: ${SECRET_NAME}. Check out Function_flows as an example.

``` yaml
# experiment.yaml
connections:
- name: aoai
  connection_type: AzureOpenAIConnection
  api_base: https://xxxxx.openai.azure.com/
  api_version: 2023-07-01-preview
  api_key: ${api_key}
  api_type: azure

# env.yaml
AZURE_OPENAI_API_KEY: ${AZURE_OPENAI_API_KEY}
```

During execution, the ${api_key} and ${AZURE_OPENAI_API_KEY} placeholders are replaced with the corresponding values from the secrets.


## Pipeline Execution

When executing the template through Jenkins pipelines, the secrets are loaded from the ENV_VARS stored as a secret file within Jenkins. The placeholders in experiment.yaml and env.yaml are replaced with the values from the ENV_VARS secret.
For example, if the ENV_VARS secret contains:

``` bash

AOAI_API_KEY=abcdefghijklmnop

AZURE_OPENAI_API_KEY=xxxxxx

```

The placeholders in experiment.yaml, flow.flex.yaml, init.json and env.yaml will be replaced in the same way as in local execution.

To ensure clarity and avoid naming conflicts, it's important to follow a specific naming convention for secrets used in this template.
When defining secrets for connections, such as API keys, the secret name should be qualified with the connection name. This helps to distinguish between secrets used for different connections. The naming convention for connection secrets is as follows:

<CONNECTION_NAME>_API_KEY

For example, if you have a connection named AOAI, the corresponding API key secret should be named AOAI_API_KEY. Only API_KEY is supported for connections.

If secrets are used within the init section of the flow.flex.yaml file, the secret name should be qualified with the parent name. This helps to identify the specific flow and context in which the secret is used. The naming convention for flow secrets is as follows:

<PARENT_ELEMENT_NAME>_<SECRET_NAME>

For example, if you have a secret named API_KEY used within the init section of a flow under MODEL_CONFIG, the corresponding secret should be named MODEL_CONFIG_API_KEY.

By adhering to the naming convention for secrets, storing them securely in the .env file or Jenkins secrets, and following the best practices for secret security, you can ensure that sensitive information remains protected while allowing seamless execution of the template in different environments.

## Create Azure service principal

Create one Azure service principal for the purpose of understanding this repository. You can add more depending on how many environments, you want to work on (Dev or Prod or Both). Service principals can be created using cloud shell, bash, powershell or from Azure UI.  If your subscription is part of an organization with multiple tenants, ensure that the Service Principal has access across tenants.

1. Copy the following bash commands to your computer and update the **spname** and **subscriptionId** variables with the values for your project. This command will also grant the **owner** role to the service principal in the subscription provided. This is required for Jenkins to properly use resources in that subscription.

    ``` bash
    spname="<provide a name to create a new sp name>"
    roleName="Owner"
    subscriptionId="<provide your subscription Id>"
    servicePrincipalName="Azure-ARM-${spname}"

    # Verify the ID of the active subscription
    echo "Using subscription ID $subscriptionID"
    echo "Creating SP for RBAC with name $servicePrincipalName, with role $roleName and in scopes     /subscriptions/$subscriptionId"

    az ad sp create-for-rbac --name $servicePrincipalName --role $roleName --scopes /subscriptions/$subscriptionId --sdk-auth

    echo "Please ensure that the information created here is properly save for future use."

1. Copy your edited commands into the Azure Shell and run them (**Ctrl** + **Shift** + **v**). If executing the commands on local machine, ensure Azure CLI is installed and successfully able to access after executing `az login` command. Azure CLI can be installed using information available [here](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)

1. After running these commands, you'll be presented with information related to the service principal. Save this information to a safe location, you'll use it later in the demo to configure Jenkins.

`NOTE: The below information should never be part of your repository and its branches. These are important secrets and should never be pushed to any branch in any repository.`

    ```json

      {
      "clientId": "<service principal client id>",
      "clientSecret": "<service principal client secret>",
      "subscriptionId": "<Azure subscription id>",
      "tenantId": "<Azure tenant id>",
      "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
      "resourceManagerEndpointUrl": "https://management.azure.com/",
      "activeDirectoryGraphResourceId": "https://graph.windows.net/",
      "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
      "galleryEndpointUrl": "https://gallery.azure.com/",
      "managementEndpointUrl": "https://management.core.windows.net/"
      }
    ```

1. Copy the output, braces included. It will be used later in the demo to configure the Jenkins environment credentials.

1. Close the Cloud Shell once the service principals are created.

## Setup runtime for Prompt flow

Prompt flow 'flows' require runtime associated with compute instance in Azure Machine Learning workspace. The template provides support for 'automatic runtime' where flows are executed within a runtime provisioned automatically during execution. The first execution might need additional time for provisioning of the runtime.

The template supports using 'automatic runtime' and compute instances. There is no configured required for using automatic runtime. However, if you want to use compute instances, you can create a compute instance in Azure Machine Learning workspace. More details about creating compute instances in Azure Machine Learning workspace is available [here](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-create-attach-compute-studio?view=azure-ml-py).

## Set up Github Repo

Fork this repository [LLMOps Prompt flow Template Repo](https://github.com/microsoft/llmops-promptflow-template) in your GitHub organization. This repo has reusable LLMOps code that can be used across multiple projects.

![fork the repository](images/fork.png)

Create a *development* branch from *main* branch and also make it as default one to make sure that all PRs should go towards it. This template assumes that the team works at a *development* branch as a primary source for coding and improving the prompt quality. Later, you can implement Jenkins pipelines that move code from the *development* branch into qa/main or execute a release process right away. Release management is not in part of this template.

![create a new development branch](images/new-branch.png)

At this time, `main` is the default branch.

![main as default branch](images/main-default.png)

From the settings page, switch the default branch from `main` to `development`

![change development as default branch](images/change-default-branch.png)

It might ask for confirmation.

![default branch confirmation](images/confirmation.png)

Eventually, the default branch in github repo should show `development` as the default branch.

![make development branch as default branch](images/default-branch.png)

The template comes with a few declarative Jenkins pipelines related to Prompt flow flows for providing a jumpstart (named_entity_recognition, web_classification and math_coding). Each scenario has 2 primary workflows and 1 optional workflow. The first one is executed during pull request(PR) e.g. [named_entity_recognition_pr_dev](../.jenkins/pipelines/named_entity_recognition_pr_dev), and it helps to maintain code quality for all PRs. Usually, this pipeline uses a smaller dataset to make sure that the Prompt flow job can be completed fast enough.

The second Jenkins pipelines [named_entity_recognition_ci_dev](../.jenkins/pipelines/named_entity_recognition_ci_dev) is executed automatically before a PR is merged into the *development* or *main* branch. The main idea of this pipeline is to execute bulk run and evaluation on the full dataset for all prompt variants. The workflow can be modified and extended based on the project's requirements.

## Set up Jenkins Credentials for Azure

From your Jenkins dashboard, select **Manage Jenkins** -> **Credentials**,  **(global) Domain** and **+ Add Credentials**. From the **Kind** dropdown box, select the **Azure Service Principal** option. Provide the service principal secret values you saved earlier: `Subscription ID`, `Client ID`, `Client Secret` and `Tenant ID`. Enter `AZURE_CREDENTIALS` for the `ID` field - this value will be used as a name/reference for the credentials inside each pipeline.

![Screenshot of Jenkins Credentials.](images/jenkins-credentials.png)

## Set up Jenkins Global variables for each environment

There are 3 variables per environment expected as Global Jenkins variables: `RESOURCE_GROUP_NAME_<env>`, `WORKSPACE_NAME_<env>` and `KEY_VAULT_NAME_<env>`.

From your Jenkins dashboard, select **Manage Jenkins** -> **System** and scroll to **Global Properties**. Add the variables and their values for each used environment. 

![Screenshot of Jenkins Global Environment Variables.](images/jenkins-environments-new-var.png)

## Setup connections for Prompt flow

Prompt flow Connections helps securely store and manage secret keys or other sensitive credentials required for interacting with LLM and other external tools, for example Azure OpenAI.

This repository has 3 examples, and all the examples use a connection named `aoai` inside, we need to set up a connection with this name if we haven’t created it before.

This repository has all the examples use Azure OpenAI model `gpt-35-turbo` deployed with the same name `gpt-35-turbo`, we need to set up this deployment if we haven’t created it before.

Please go to Azure Machine Learning workspace portal, click `Prompt flow` -> `Connections` -> `Create` -> `Azure OpenAI`, then follow the instructions to create your own connections called `aoai`. Learn more on [connections](https://learn.microsoft.com/en-us/azure/machine-learning/prompt-flow/concept-connections?view=azureml-api-2). The samples use a connection named "aoai" connecting to a gpt-35-turbo model deployed with the same name in Azure OpenAI. This connection should be created before executing the out-of-box flows provided with the template.

![aoai connection in Prompt flow](images/connection.png)

The configuration for connection used while authoring the repo:

![connection details](images/connection-details.png)

## Set up Secrets in Jenkins

### Azure Container Registry

Create Jenkins Credentials of the type **Secret Text** named `DOCKER_IMAGE_REGISTRY` with information related to Docker Image Registry. The value for this secret is also a json string with given structure. Create one json object for each registry. As of now, Azure Container Registry are supported and more will get added soon. Information for each registry can be obtained from Azure Container Registry resource.

It is important to note that there can be any number of variables and each storing Azure Container Registry details as shown next and they can be named anything permissible based on your preference. You should use the same variable in your use-case related CI pipelines. The template by default uses `DOCKER_IMAGE_REGISTRY` for this purpose.

```json
[
	{
		"registry_name" : "xxxxxxxx",
		"registry_server" : "xxxx.azurecr.io",
		"registry_username" : "xxxxxxxxx",
		"registry_password": "xxxxxxxxxxxxxx"
	}
]

```
### Environment Variables

Create another Jenkins secret credential using secret file option named 'ENV_VARS'. The data for this secret is same as you put in .env file. Each line is a name=value pair and the values are separated by a newline. The values can be anything permissible based on your preference. The keys should be in upper case. You should use the same key in your use-case related CI workflows. This includes you python code, experiment.yaml and workflows. The template by default uses 'ENV_VARS' for this purpose.

The environment variables for Prompt Flow Connections should follow a specific naming convention to ensure clarity and consistency. The format is as follows:

<CONNECTION_NAME>_API_KEY


- `<CONNECTION_NAME>`: Replace this with the name of the Prompt Flow Connection for which the API key is associated. The connection name should be in uppercase.
- `_API_KEY`: This suffix indicates that the environment variable represents an API key.


```bash

```.env

AOAI_API_KEY=xxxxxxxxxxxx
ANY_OTHER_VALUE=xxxxxxxxxxxx


```

## Cloning the repo

 Now, we can clone the forked repo on your local machine using command shown here. Replace the repo url with your url.

``` bash
git clone https://github.com/ritesh-modi/llmops-promptflow-template.git

cd llmops-promptflow-template

git branch

```

Create a new feature branch using the command shown here. Replace the branch name with your preferred name.

``` bash

git checkout -b featurebranch

```

The pipeline expects the variables `RESOURCE_GROUP_NAME`, `WORKSPACE_NAME` and `KEY_VAULT_NAME` to be available as environment variable (this should have already been created and set [here](#set-up-jenkins-global-variables-for-each-environment)). These variables should contain the values of the Azure resources in the dev environment. To add a new environment, you must create the variables for that staging environment with the correct environment suffix. These variable names can then be used in the new pipelines created for that environment.

The rest of the pipeline configurations will be read from the `experiment.yaml` file (see file [description](./the_experiment_file.md) and [specs](./experiment.yaml)); and from the `configs/deployment_config.json` file for the deployment.

Before running the deployment pipelines, you need to make changes to `configs/deployment_config.json`:
- Update the `ENDPOINT_NAME` and `CURRENT_DEPLOYMENT_NAME` if you want to deploy to Azure Machine Learning compute
- Or update the `CONNECTION_NAMES`, `REGISTRY_NAME`, `REGISTRY_RG_NAME`, `APP_PLAN_NAME`, `WEB_APP_NAME`, `WEB_APP_RG_NAME`, `WEB_APP_SKU`, and `USER_MANAGED_ID`if you want to deploy to Azure Web App.

### Update deployment_config.json in config folder

Modify the configuration values in the `deployment_config.json` file for each environment. These are required for deploying Prompt flows in Azure ML. Ensure the values for `ENDPOINT_NAME` and `CURRENT_DEPLOYMENT_NAME` are changed before pushing the changes to remote repository.

- `ENV_NAME`: This indicates the environment name, referring to the "development" or "production" or any other environment where the prompt will be deployed and used in real-world scenarios.
- `TEST_FILE_PATH`: The value represents the file path containing sample input used for testing the deployed model.
- `ENDPOINT_NAME`: The value represents the name or identifier of the deployed endpoint for the prompt flow.
- `ENDPOINT_DESC`: It provides a description of the endpoint. It describes the purpose of the endpoint, which is to serve a prompt flow online.
- `DEPLOYMENT_DESC`: It provides a description of the deployment itself.
- `PRIOR_DEPLOYMENT_NAME`: The name of prior deployment. Used during A/B deployment. The value is "" if there is only a single deployment. Refer to CURRENT_DEPLOYMENT_NAME property for the first deployment.
- `PRIOR_DEPLOYMENT_TRAFFIC_ALLOCATION`:  The traffic allocation of prior deployment. Used during A/B deployment. The value is "" if there is only a single deployment. Refer to CURRENT_DEPLOYMENT_TRAFFIC_ALLOCATION property for the first deployment.
- `CURRENT_DEPLOYMENT_NAME`: The name of current deployment.
- `CURRENT_DEPLOYMENT_TRAFFIC_ALLOCATION`: The traffic allocation of current deployment. A value of 100 indicates that all traffic is directed to this deployment.
- `DEPLOYMENT_VM_SIZE`: This parameter specifies the size or configuration of the virtual machine instances used for the deployment.
- `DEPLOYMENT_INSTANCE_COUNT`:This parameter specifies the number of instances (virtual machines) that should be deployed for this particular configuration.
- `ENVIRONMENT_VARIABLES`: This parameter represents a set of environment variables that can be passed to the deployment.

Kubernetes deployments have additional properties - `COMPUTE_NAME`, `DEPLOYMENT_VM_SIZE`, `CPU_ALLOCATION` and `MEMORY_ALLOCATION` related to infrastructure and resource requirements. These should also be updates with your values before executing Kubernetes based deployments.

Azure Web App deployments do not have similar properties as that of Kubernetes and Azure ML compute. For Azure Web App, following properties should be updated.

- `ENV_NAME`: This indicates the environment name, referring to the "development" or "production" or any other environment where the prompt will be deployed and used in real-world scenarios.
- `TEST_FILE_PATH`: The value represents the file path containing sample input used for testing the deployed model.
- `CONNECTION_NAMES`: The name of the connections used in standard flow in json aray format. e.g. ["aoai", "another_connection"],
- `REGISTRY_NAME`: This is the name of the Container Registry that is available in the `DOCKER_IMAGE_REGISTRY` secret. Based on this name, appropriate registry details will be used for `Docker` image management.
- `REGISTRY_RG_NAME`: This is the name of the resource group related to the Container Registry. It is used for downloading the Docker Image.
- `APP_PLAN_NAME`: Name of the App Services plan. It will be provisioned by the pipeline.
- `WEB_APP_NAME`: Name of the Web App. It will be provisioned by the pipeline.
- `WEB_APP_RG_NAME`:  Name of the resource group related to App Service plan and Web App. It will be provisioned by the pipeline.
- `WEB_APP_SKU`: This is the `SKU` (size) of the Web App. e.g. "B3"
- `USER_MANAGED_ID`: This is the name of the user defined managed id created during deployment associated with the Web App.

`NOTE: For Docker based deployments, ensure to add promptflow, promptflow[azure], promptflow-tools packages in each flow's requirements.txt file`. Check-out existing use-cases (named_entity_recognition, math_coding, web_classification) for examples.`

Now, push the new feature branch to the newly forked repo.

``` bash

git add .
git commit -m "changed code"
git push -u origin featurebranch

```

## Configure pipelines in Jenkins

In this example, all pipelines will be created for the **Named Entity Recognition Flow**, feel free to use instead one of the other supported flows (Math Coding or Web Classification) for your setup.

In your Jenkins environment create a new **Pipeline** with the name `named_entity_recognition_pr_dev` and select the option to define the **Pipeline Script from SCM**. Select **Git** as the Source Control option, and provide the **Repository URL** for your forked repository. In the **Branch Specifier** field, provide `*/<your-featurebranch>`. For the **Script Path** field, provide the path to the Jenkinsfile for the pipeline you're creating, which is `.jenkins/pipelines/named_entity_recognition_pr_dev`, and press **Save**.

These steps shoud be repeated for all pipelines which are required to run the PR and CI/CD pipelines for the NER flow. In the table below you can find the list of pipeline names, branches and script paths required for each pipeline.

| Pipeline Name |  Branch Specifier | Script Path |
| ------------- | ----------- | ----------- |
| named_entity_recognition_pr_dev    | `*/<your-featurebranch>` |  `.jenkins/pipelines/named_entity_recognition_pr_dev` |
| platform_pr_dev    | `*/<your-featurebranch>` | `.jenkins/pipelines/platform_pr_dev` |
| named_entity_recognition_ci_dev    | `*/development` | `.jenkins/pipelines/named_entity_recognition_ci_dev` |
| platform_ci_dev   | `*/development` |`.jenkins/pipelines/platform_ci_dev` |
| platform_cd_dev   | `*/development` |`.jenkins/pipelines/platform_cd_dev` |

## Configure actions in Jenkins

Many of the Jenkins pipelines trigger specific actions which are stored in the [.jenkins/jobs/](../.jenkins/jobs/) directory. Therefore it is necessary to configure Jenkins pipelines for each of the individual actions.

First, create a **+ New Item** of the type **Folder** and call it `jobs`. Inside the `jobs` folder, create pipelines for each action file in the same way you did for the pipelines, using the **Pipeline Script from SCM** option. The details for which branch and script path to use are in the table below:

| Pipeline Name |  Branch Specifier | Script Path |
| ------------- | ----------- | ----------- |
| aml_real_deployment    | `*/development` |  `.jenkins/jobs/aml_real_deployment` |
| build_validation    | `*/<your-featurebranch>` | `.jenkins/jobs/build_validation` |
| kubernetes_deployment   | `*/development` | `.jenkins/jobs/kubernetes_deployment` |
| prepare_docker_image   | `*/development` | `.jenkins/jobs/prepare_docker_image` |
| webapp_deployment   | `*/development` | `.jenkins/jobs/webapp_deployment` |

## Set up Trigger Webhook

Both the PR and CI pipelines for each use case will be triggered by different events. The PR pipeline will be triggered whenever a PR is opened on a `feature branch`, and the CI pipeline will be triggered once a merge is done on the `development` branch. To send these events from the GitHub repository to Jenkins it's necessary to define a `Webhook`. This can be done in the **Settings** tab of your GitHub repository, then going to the **Webhooks** tab and press **Add webhook**.

In the **payload** section, provide the following url:
`http://<your Jenkins ip address>:<the port on which Jenkins is running>/generic-webhook-trigger/invoke?token=`.
In the **secret** section, provide a random string with high entropy to be used as a token by Jenkins.
Select **Send me everything** from the options on which events to send through this webhook. Then press **Add Webhook**.

![Create a GitHub webhook](images/jenkins-webhook-gh.png)

## Create Jenkins Credentials for Webhook Token Secret

Create another set of **Jenkins Credentials** of type **Secret Text** with the name `WEBHOOK-TOKEN-SECRET`, to store the value of the GitHub Webhook secret, such that it can be used inside the pipeline.

Inside the Jenkins pipelines, the `GenericTrigger` block is already set up to define the regular expressions which ensure that the pipeline is triggered only when certain events are part of the webhook request, such as the PR being `opened`, `reopened` or `synchronized` as can be seen in this example:

```groovy
    triggers {
        GenericTrigger(
                genericVariables: [
                    [key: 'action', value: '$.action']
                ],
                genericHeaderVariables: [
                ],
                causeString: 'Triggered on $action',
                tokenCredentialId: 'WEBHOOK-TOKEN-SECRET',
                printContributedVariables: true,
                printPostContent: false,
                silentResponse: false,
                regexpFilterText: '$action',
                regexpFilterExpression: '^(opened|reopened|synchronize)$'
        )
    }
```

## Raise PR to trigger pipeline

Raise a new PR to merge code from `feature branch` to the `development` branch. Ensure that the PR from feature branch to development branch happens within your repository and organization.

![raise a new PR](images/pr.png)

This should start the process of executing the Named Entity Recognition PR pipeline.

![PR pipeline execution](images/jenkins-pr-trigger.png)

After the execution is complete, the code can be merged to the `development` branch. Upon merging into `development` the CI Pipeline will be triggered, which in its turn triggers the CD Pipeline. This CI/CD pipeline will target the `dev` environment for deployment.
Now a new PR can be opened from `development` branch to the `main` branch. This should execute both the PR as well as the CI/CD pipeline.

## Update configurations for Prompt flow and Jenkins

There are multiple configuration files for enabling Prompt flow run and evaluation in Azure ML and Jenkins

### Update the experiment.yaml file

To make any changes to your experiment set-up, refer to the `experiment.yaml` in the base path of your use-case. This file configures your use-case including flows and datasets. (see file [description](./the_experiment_file.md) and [specs](./experiment.yaml) for more details).

### Update data folder with data files

Add your data into the `data` folder under the use case folder. It supports `jsonl` files and the examples already contains data files for both running and evaluating Prompt flows.

### Update Standard and evaluation flows

The `flows` folder contains one folder for each standard and evaluation flow. Each example in the repository already has these flows.

### Update Environment related dependencies

The `environment folder` contains dockerfile file for webapp and function app deployments. Any additional dependencies needed by the flow should be added to it. This file is used during deployment process.

### Update test data

The `sample-request.json` file contains a single test data used for testing the online endpoint after deployment in the pipeline. Each example has its own `sample-request.json` file and for custom flows, it should be updated to reflect test data needed for testing.

## Example Prompt Run, Evaluation and Deployment Scenario

There are three examples in this template. While `named_entity_recognition` and `math_coding` have the same functionality, `web_classification` has multiple evaluation flows and datasets for the dev environment. This is a flow in general across all examples.

This Jenkins CI workflow contains the following steps:

**Run Prompts in Flow**
- Upload bulk run dataset
- Bulk run prompt flow based on dataset
- Bulk run each prompt variant

**Evaluate Results**
- Upload ground test dataset
- Execution of multiple evaluation flows for a single bulk run (only for web_classification)
- Evaluation of the bulk run result using single evaluation flow (for others)

**Register Prompt flow LLM App**
- Register Prompt flow as a Model in Azure Machine Learning Model Registry

**Deploy and Test LLM App**
- Deploy the Flow as a model to the development environment either as Kubernetes or Azure ML Compute endpoint
- Assign RBAC permissions to the newly deployed endpoint to Key Vault and Azure ML workspace
- Test the model/promptflow realtime endpoint.

**Run post production deployment evaluation**
- Upload the sampled production log dataset
- Execute the evaluation flow on the production log dataset
- Generate the evaluation report

**Run promptflow in AML Pipeline as parallel component**
- It reuses the already registered data assets for input.
- Runs the promptflow in AML Pipeline as a parallel component, where we can control the concurrency and parallelism of the promptflow execution. For more details refer [here](https://microsoft.github.io/promptflow/tutorials/pipeline.html).
- The output of the promptflow is stored in the Azure ML workspace.

### Online Endpoint

1. After the CI pipeline for an example scenario has run successfully, depending on the configuration it will either deploy to

     ![Managed online endpoint](./images/online-endpoint.png) or to a Kubernetes compute type

     ![Managed online endpoint](./images/kubernetes.png)

2. Once pipeline execution completes, it would have successfully completed the test using data from `sample-request.json` file as well.

     ![online endpoint test in pipeline](./images/jenkins-pipeline-test.png)

## Moving to production

The example scenario can be run and deployed both for Dev environments. When you are satisfied with the performance of the prompt evaluation pipeline, Prompt flow model, and deployment in development, additional pipelines similar to `dev` pipelines can be replicated and deployed in the Production environment.

The sample Prompt flow run & evaluation and Jenkins pipelines can be used as a starting point to adapt your own prompt engineering code and data.
