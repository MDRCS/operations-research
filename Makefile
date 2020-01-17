PYTHON = python3
TEST:
	 ${PYTHON} amphibians_coexistence_model.py 
	 ${PYTHON} food_distribution.py run
	 ${PYTHON} Blending_gas_problem.py raw	
	 ${PYTHON} Blending_gas_problem.py ref	
	 ${PYTHON} Blending_gas_problem.py run	
	 ${PYTHON} project_management.py data
	 ${PYTHON} project_management.py run
	 ${PYTHON} soap_manufacturing.py resources
	 ${PYTHON} soap_manufacturing.py target
	 ${PYTHON} soap_manufacturing.py cost
	 ${PYTHON} soap_manufacturing.py inventory
	 ${PYTHON} soap_manufacturing.py run
