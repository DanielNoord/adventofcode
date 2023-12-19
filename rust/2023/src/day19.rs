use std::{collections::HashMap, str::FromStr};

#[derive(Debug)]
struct Rating {
    x: u64,
    m: u64,
    a: u64,
    s: u64,
}

impl FromStr for Rating {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // Trust me this works...
        let subs: Vec<&str> = s.split('=').collect();
        Ok(Rating {
            x: subs[1].split(',').next().unwrap().parse().unwrap(),
            m: subs[2].split(',').next().unwrap().parse().unwrap(),
            a: subs[3].split(',').next().unwrap().parse().unwrap(),
            s: subs[4].strip_suffix('}').unwrap().parse().unwrap(),
        })
    }
}

fn do_workflow(workflow: &str, rating: &Rating) -> String {
    for step in workflow.split(',') {
        // This is always the final step in a workflow so we exit early
        if !step.contains(':') {
            return step.to_string();
        };

        let (check, result) = step.split_once(':').unwrap();
        let result = result.to_string();

        let mut check_chars = check.chars();
        let value_to_check = match check_chars.next().unwrap() {
            'x' => rating.x,
            'm' => rating.m,
            'a' => rating.a,
            's' => rating.s,
            _ => panic!("Unexpected indicator"),
        };

        let comparator = check_chars.next().unwrap();
        let value_to_compare: u64 = String::from_iter(check_chars).parse().unwrap();

        match comparator {
            '<' => {
                if value_to_check < value_to_compare {
                    return result;
                }
            }
            '>' => {
                if value_to_check > value_to_compare {
                    return result;
                }
            }
            _ => panic!("Unexpected comparator"),
        }
    }
    panic!("Should have found a step without a ':'");
}

fn get_workflow_map(workflows: &str) -> HashMap<&str, &str> {
    let mut workflow_map: HashMap<&str, &str> = HashMap::new();

    // Since rust is fast enough we don't need to convert each workflow to a function
    // We can just store the workflow as string and parse it everytime :)
    for workflow in workflows.lines() {
        // This parsing "just works"
        let (name, flow) = workflow.split_once('{').unwrap();
        let flow = flow.strip_suffix('}').unwrap();

        workflow_map.insert(name, flow);
    }
    workflow_map
}

pub fn part1(input: &str) -> String {
    let (workflows, ratings) = input.split_once("\n\n").unwrap();
    let workflow_map: HashMap<&str, &str> = get_workflow_map(workflows);

    let mut total = 0;
    // Initialize the endpoints once, don't actually know if this matters
    let accepted = String::from("A");
    let rejected = String::from("R");

    for rating in ratings.lines() {
        let rating: Rating = rating.parse().unwrap();
        // Initial position
        let mut current_step: String = String::from("in");

        loop {
            if current_step == accepted {
                total += rating.x + rating.m + rating.a + rating.s;
                break;
            }
            if current_step == rejected {
                break;
            }

            current_step =
                do_workflow(workflow_map.get(current_step.as_str()).unwrap(), &rating)
        }
    }

    assert!(total == 409898, "Should be 409898");
    total.to_string()
}

#[derive(Debug, Clone, Copy)]
struct RatingPartTwo {
    x: (u64, u64),
    m: (u64, u64),
    a: (u64, u64),
    s: (u64, u64),
}

impl RatingPartTwo {
    fn get_arm_to_change(&mut self, indicator: char) -> &mut (u64, u64) {
        // Get a reference to the arm of the Rating that we should change depending on the indicator
        match indicator {
            'x' => &mut self.x,
            'm' => &mut self.m,
            'a' => &mut self.a,
            's' => &mut self.s,
            _ => panic!(),
        }
    }
}

fn do_workflow_part_two(
    workflow: &str,
    // Pass mutable as we keep updating it to be a new rating that should be 'stepped' through
    mut rating: RatingPartTwo,
) -> Vec<(String, RatingPartTwo)> {
    let mut new_ratings: Vec<(String, RatingPartTwo)> = Vec::new();

    for step in workflow.split(',') {
        // This is always the final step in a workflow so we exit early
        if !step.contains(':') {
            new_ratings.push((step.to_string(), rating));
            break;
        };

        let (check, result) = step.split_once(':').unwrap();
        let result = result.to_string();

        let mut check_chars = check.chars();
        let letter_indicator = check_chars.next().unwrap();

        let comparator = check_chars.next().unwrap();
        let value_to_compare: u64 = String::from_iter(check_chars).parse().unwrap();

        // Get the range we are comparing against, we don't need the mut reference here
        let range_to_check = rating.get_arm_to_change(letter_indicator).to_owned();
        match comparator {
            '<' => {
                if range_to_check.0 < value_to_compare {
                    if range_to_check.1 > value_to_compare {
                        // This rating will be parsed separately and added to the queue
                        let mut new_rating = rating;
                        *new_rating.get_arm_to_change(letter_indicator) =
                            (range_to_check.0, value_to_compare - 1);
                        new_ratings.push((result, new_rating));

                        // Update the current rating so we can keep going through the steps of this
                        // workflow
                        *rating.get_arm_to_change(letter_indicator) =
                            (value_to_compare, range_to_check.1);
                    } else {
                        // For my input and test data there was never a path where the full range
                        // was under the comparison value
                        panic!(
                            "Full range is below comparator (<) at {}",
                            value_to_compare
                        );
                    }
                } else {
                    // For my input and test data there was never a path where the full range was
                    // above the comparison value
                    panic!("Range is above comparator (<) at {}", value_to_compare);
                }
            }
            '>' => {
                if range_to_check.0 < value_to_compare {
                    if range_to_check.1 > value_to_compare {
                        // This rating will be parsed separately and added to the queue
                        let mut new_rating = rating;
                        *new_rating.get_arm_to_change(letter_indicator) =
                            (value_to_compare + 1, range_to_check.1);
                        new_ratings.push((result, new_rating));

                        // Update the current rating so we can keep going through the steps of this
                        // workflow
                        *rating.get_arm_to_change(letter_indicator) =
                            (range_to_check.0, value_to_compare);
                    } else {
                        // For my input and test data there was never a path where the full range
                        // was under the comparison value
                        panic!(
                            "Full range is below comparator (>) at {}",
                            value_to_compare
                        );
                    }
                } else {
                    // For my input and test data there was never a path where the full range was
                    // above the comparison value
                    panic!("Range is above comparator (>) at {}", value_to_compare)
                }
            }
            _ => panic!("Can't handle comparator {}", comparator),
        }
    }

    new_ratings
}

pub fn part2(input: &str) -> String {
    let (workflows, _) = input.split_once("\n\n").unwrap();
    let workflow_map: HashMap<&str, &str> = get_workflow_map(workflows);

    // Initialize the endpoints once, (again) don't actually know if this matters
    let accepted = String::from("A");
    let rejected = String::from("R");

    let mut total = 0;
    // Use a queue of Ratings that not have reached either accepted or rejected
    let mut queue: Vec<(String, RatingPartTwo)> = vec![(
        String::from("in"),
        RatingPartTwo {
            x: (1, 4000),
            m: (1, 4000),
            a: (1, 4000),
            s: (1, 4000),
        },
    )];

    while let Some(entry) = queue.pop() {
        if entry.0 == accepted {
            // Get the range per arm and increment + 1 as the range is inclusive
            let x_total = entry.1.x.1 - entry.1.x.0 + 1;
            let m_total = entry.1.m.1 - entry.1.m.0 + 1;
            let a_total = entry.1.a.1 - entry.1.a.0 + 1;
            let s_total = entry.1.s.1 - entry.1.s.0 + 1;

            total += x_total * m_total * a_total * s_total;
        } else if entry.0 != rejected {
            // Add the new ratings to the queue so we can process them
            queue.extend(do_workflow_part_two(
                workflow_map.get(entry.0.as_str()).unwrap(),
                entry.1,
            ))
        }
    }

    assert!(total == 113057405770956, "Should be 113057405770956");
    total.to_string()
}
