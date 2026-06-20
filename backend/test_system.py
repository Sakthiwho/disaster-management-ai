from backend.disaster_controller import DisasterController


controller = DisasterController()

result = controller.run_disaster_simulation()

print("\n🚨 DISASTER RESPONSE SYSTEM OUTPUT\n")

print(result)