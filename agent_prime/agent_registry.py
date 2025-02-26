from speciality_agents.intergration_agent.intergration_agent import create_intergration_agent
from speciality_agents.network_agent.network_agent import create_network_agent
from speciality_agents.ml_model_creation_agent.ml_model_creation_agent import create_ml_model_creation_agent
from speciality_agents.data_agent.data_agent import create_data_agent
from speciality_agents.automation_agent.automation_agent import create_automation_agent
from speciality_agents.security_agent.security_agent import create_security_agent
from speciality_agents.business_agent.business_agent import create_business_agent
from speciality_agents.development_agent.development_agent import create_development_agent
from speciality_agents.system_agent.system_agent import create_system_agent
from speciality_agents.media_agent.media_agent import create_media_agent
from speciality_agents.file_agent.file_agent import create_file_agent
from speciality_agents.web_agent.web_agent import create_web_agent
from speciality_agents.example_agent.example_agent import create_example_agent

def map_agent(tool):
    mapper_function = {
        'WEB': create_web_agent,
        'FILE': create_file_agent,
        'DATA': create_data_agent,
        'SYSTEM': create_system_agent,
        'NETWORK': create_network_agent,
        'DEVELOPMENT': create_development_agent,
        'BUSINESS': create_business_agent,
        'MEDIA': create_media_agent,
        'SECURITY': create_security_agent,
        'AUTOMATION': create_automation_agent,
        'ML_MODEL_CREATION': create_ml_model_creation_agent,
        'INTEGRATION': create_intergration_agent,
        'EXAMPLE': create_example_agent
    }
    return mapper_function.get(tool)



if __name__ == '__main__':
    run = map_agent(tool='')