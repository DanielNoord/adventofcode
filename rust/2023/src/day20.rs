use num::Integer;
use std::collections::{HashMap, VecDeque};

#[derive(Debug, Clone)]
struct Module {
    is_conjunction: bool,
    turned_on: bool,
    inputs: HashMap<String, Pulse>,
    destinations: Vec<String>,
}

#[derive(Debug, Clone, PartialEq)]
enum Pulse {
    High,
    Low,
}

fn map_modules(input: &str) -> (HashMap<String, Module>, Vec<String>) {
    // Map each module name to an actual Module object
    let mut modules: HashMap<String, Module> = HashMap::new();
    // Store a module name to its inputs so we can update it after seeing all modules once
    let mut inputs: HashMap<String, Vec<String>> = HashMap::new();
    let mut rx_inputs: Vec<String> = Vec::new();

    for line in input.lines() {
        let (module_string, destination_list) = line.split_once(" -> ").unwrap();

        let module_name = if module_string != "broadcaster" {
            // If not broadcaster we should strip the indicator in postition 0
            let stripped_name = &module_string.chars().collect::<Vec<char>>()[1..];
            let iter_stripped = stripped_name.iter();
            String::from_iter(iter_stripped)
        } else {
            String::from(module_string)
        };

        let destinations = destination_list
            .split(", ")
            .map(|e| e.to_string())
            .collect::<Vec<String>>();

        // Store this module as an input for its destination so we can later add those
        // We haven't seen all modules yet so can't insert in place
        for destination in &destinations {
            inputs
                .entry(destination.to_owned())
                .or_default()
                .push(module_name.clone());
        }

        let module = Module {
            is_conjunction: module_string.starts_with('&'),
            turned_on: false,
            inputs: HashMap::new(),
            destinations,
        };

        modules.insert(module_name, module);
    }

    for (dest, inputs) in inputs {
        if dest == "rx" {
            rx_inputs = inputs.clone();
        }
        // There are some destinations that are sinks, and are not included in modules
        if let Some(module) = modules.get_mut(&dest) {
            for input in inputs {
                // Each input node starts on Low
                module.inputs.insert(input, Pulse::Low);
            }
        }
    }
    (modules, rx_inputs)
}

fn send_pulse(
    pulse: Pulse,
    module_name: String,
    origin: String,
    modules: &mut HashMap<String, Module>,
) -> Vec<(Pulse, String, String)> {
    let mut new_pulses: Vec<(Pulse, String, String)> = Vec::new();
    let module = modules.get_mut(&module_name).unwrap();

    // Special cased module that just sends recieved Pulse
    if module_name == "broadcaster" {
        for destination in module.destinations.iter() {
            new_pulses.push((
                pulse.clone(),
                destination.to_string(),
                module_name.clone(),
            ));
        }
    // These are called flip-flop modules
    } else if !module.is_conjunction {
        match pulse {
            // No action
            Pulse::High => (),
            // Action depending on current state of the module
            Pulse::Low => {
                if module.turned_on {
                    for destination in module.destinations.iter() {
                        new_pulses.push((
                            Pulse::Low,
                            destination.to_string(),
                            module_name.clone(),
                        ));
                    }
                } else {
                    for destination in module.destinations.iter() {
                        new_pulses.push((
                            Pulse::High,
                            destination.to_string(),
                            module_name.clone(),
                        ));
                    }
                }
                module.turned_on = !module.turned_on;
            }
        }
    } else {
        // First make sure to update the "state" of the input module
        let current_pulse_for_origin = module.inputs.get_mut(&origin).unwrap();
        *current_pulse_for_origin = pulse.clone();

        // Send pulse according to state of all inputs
        if module.inputs.values().all(|e| e == &Pulse::High) {
            for destination in module.destinations.iter() {
                new_pulses.push((
                    Pulse::Low,
                    destination.to_string(),
                    module_name.clone(),
                ));
            }
        } else {
            for destination in module.destinations.iter() {
                new_pulses.push((
                    Pulse::High,
                    destination.to_string(),
                    module_name.clone(),
                ));
            }
        }
    }

    new_pulses
}

pub fn part1(input: &str) -> String {
    let (mut modules, _) = map_modules(input);
    let mut low_pulse_count = 0;
    let mut high_pulse_count = 0;

    // We only need 1000 loops
    for _ in 0..1000 {
        // According to the stdlib docs, this is a good way to do .pop(0)
        let mut pulse_queue: VecDeque<(Pulse, String, String)> = VecDeque::new();
        pulse_queue.push_back((
            Pulse::Low,
            String::from("broadcaster"),
            "".to_string(),
        ));

        while let Some(entry) = pulse_queue.pop_front() {
            match entry.0 {
                Pulse::Low => low_pulse_count += 1,
                Pulse::High => high_pulse_count += 1,
            };

            // There are some 'sink' modules that are not actual modules and should be skipped
            if !modules.contains_key(&entry.1) {
                continue;
            }
            pulse_queue.extend(send_pulse(entry.0, entry.1, entry.2, &mut modules));
        }
    }

    let result = high_pulse_count * low_pulse_count;
    assert!(result == 812609846, "Should be 812609846");
    result.to_string()
}

pub fn part2(input: &str) -> String {
    let (mut modules, rx_targets) = map_modules(input);
    // From looking at the data we know that this is only target
    let rx_target = rx_targets[0].clone();

    // These are the Modules for which we want to find cycles, looking at the data it is the
    // first conjunction node before 'rx'
    let mut targets: HashMap<String, u64> = HashMap::new();
    for sub_target in &modules.get(&rx_target).unwrap().inputs {
        targets.insert(sub_target.0.clone(), 0);
    }

    let mut push_count: u64 = 0;
    loop {
        push_count += 1;

        // According to the stdlib docs, this is a good way to do .pop(0)
        let mut pulse_queue: VecDeque<(Pulse, String, String)> = VecDeque::new();
        pulse_queue.push_back((
            Pulse::Low,
            String::from("broadcaster"),
            "".to_string(),
        ));

        while let Some(entry) = pulse_queue.pop_front() {
            // This is so slow, but it is late and I'm happy I got something that sort of works
            for (target, cycle_count) in targets.iter_mut() {
                if modules
                    .get_key_value(&rx_target)
                    .unwrap()
                    .1
                    .clone()
                    .inputs
                    .get(target)
                    .unwrap()
                    == &Pulse::High
                    // We also need to check we don't double count the same cycle
                    && cycle_count != &push_count
                {
                    *cycle_count = push_count - *cycle_count;
                }
            }

            // Skip 'sink' modules that are not actual modules, such as 'rx'
            if !modules.contains_key(&entry.1) {
                continue;
            }

            pulse_queue.extend(send_pulse(entry.0, entry.1, entry.2, &mut modules));
        }

        // Probably a better way to do this
        if targets.values().all(|e| e != &0) {
            break;
        }
    }

    // Hey, it's the LCM again
    let result: u64 = targets
        .iter()
        .map(|e| e.1)
        .copied()
        .reduce(|acc, e| acc.lcm(&e))
        .unwrap();

    assert!(result == 245114020323037, "Should be 245114020323037");
    result.to_string()
}
