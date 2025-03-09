#!/usr/bin/env python3
"""
Example of creating a UML State Diagram using the PyDiagrams library.

This example demonstrates creating a state diagram for a door lock system,
showing different states and transitions based on events.
"""

import os
import sys

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pydiagrams import StateDiagram
from pydiagrams.diagrams.uml.state_diagram import (
    State, InitialState, FinalState, CompositeState,
    ChoicePseudostate, TransitionType
)


def create_example_state_diagram():
    """
    Create a UML State Diagram for a door lock system.
    
    The diagram shows the different states of an electronic door lock
    including locked, unlocked, and various error states.
    
    Returns:
        The path to the rendered diagram file.
    """
    # Create a new state diagram
    diagram = StateDiagram("Door Lock State Diagram")
    
    # Create states
    initial = diagram.create_initial_state()
    locked = diagram.create_state("Locked")
    locked.add_entry_activity("turn_on_red_led()")
    locked.add_do_activity("display_locked_status()")
    
    unlocked = diagram.create_state("Unlocked")
    unlocked.add_entry_activity("turn_on_green_led()")
    unlocked.add_exit_activity("beep()")
    
    authenticating = diagram.create_state("Authenticating")
    authenticating.add_entry_activity("start_timer()")
    authenticating.add_exit_activity("stop_timer()")
    
    error = diagram.create_state("Error")
    error.add_entry_activity("flash_red_led()")
    error.add_do_activity("display_error_message()")
    
    maintenance = diagram.create_state("Maintenance")
    maintenance.add_internal_transition("reset", "clear_error_log()")
    
    # Create a composite state for the alarm
    alarm_active = diagram.create_composite_state("Alarm Active")
    alarm_active.add_entry_activity("start_alarm()")
    alarm_active.add_exit_activity("stop_alarm()")
    
    # Substates for the alarm
    silent_alarm = diagram.create_state("Silent Alarm")
    silent_alarm.add_do_activity("notify_security()")
    
    audible_alarm = diagram.create_state("Audible Alarm")
    audible_alarm.add_do_activity("sound_siren()")
    
    # Add substates to the composite state
    alarm_active.add_substate(silent_alarm)
    alarm_active.add_substate(audible_alarm)
    
    # Create a choice pseudostate for authentication result
    auth_choice = diagram.create_choice_pseudostate()
    
    # Create a final state
    final = diagram.create_final_state()
    
    # Create transitions
    diagram.create_transition(
        initial, locked, 
        effect="initialize_system()"
    )
    
    diagram.create_transition(
        locked, authenticating, 
        trigger="card_swiped", 
        effect="read_card_data()"
    )
    
    diagram.create_transition(
        authenticating, auth_choice, 
        trigger="authentication_completed"
    )
    
    diagram.create_transition(
        auth_choice, unlocked, 
        guard="is_authorized", 
        effect="log_access()"
    )
    
    diagram.create_transition(
        auth_choice, error, 
        guard="!is_authorized", 
        effect="log_failed_attempt()"
    )
    
    diagram.create_transition(
        unlocked, locked, 
        trigger="timeout", 
        effect="secure_door()"
    )
    
    diagram.create_transition(
        unlocked, locked, 
        trigger="close_button_pressed", 
        effect="secure_door()"
    )
    
    diagram.create_transition(
        error, locked, 
        trigger="reset_button_pressed", 
        effect="clear_errors()"
    )
    
    diagram.create_transition(
        error, alarm_active, 
        trigger="multiple_failures", 
        guard="failure_count > 3", 
        effect="trigger_alarm()"
    )
    
    diagram.create_transition(
        alarm_active, maintenance, 
        trigger="key_switch_activated", 
        effect="enter_maintenance_mode()"
    )
    
    diagram.create_transition(
        maintenance, final, 
        trigger="shutdown_command", 
        effect="power_off()"
    )
    
    # Internal transitions within alarm_active state
    diagram.create_transition(
        silent_alarm, audible_alarm, 
        trigger="timeout", 
        guard="alarm_duration > 60", 
        effect="escalate_alarm()"
    )
    
    # Ensure the output directory exists
    os.makedirs("output", exist_ok=True)
    
    # Render the diagram to an SVG file
    output_path = "output/door_lock_state_diagram.svg"
    diagram.render(output_path)
    
    print(f"Diagram rendered to: {output_path}")
    return output_path


if __name__ == "__main__":
    create_example_state_diagram() 