use std::str::FromStr;

fn get_hash_value(string: &str) -> usize {
    let mut value = 0;
    for character in string.chars() {
        value += character as u32;
        value *= 17;
        value %= 256;
    }
    value as usize
}

pub fn part1(input: &str) -> String {
    let result: usize = input.split(',').map(get_hash_value).sum();

    assert!(result == 504449, "Should be 504449");
    result.to_string()
}

#[derive(Clone, Debug)]
enum Action {
    Remove,
    Add,
}

#[derive(Clone, Debug)]
struct Lens {
    label: String,
    action: Action,
    // Get a usize as we're multiplying with indices later
    focal_length: usize,
}

impl FromStr for Lens {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // Return Lenses depending on their last character
        if s.ends_with('-') {
            Ok(Lens {
                label: s[0..s.len() - 1].to_string(),
                action: Action::Remove,
                // Just a sensible default, never used anyway
                focal_length: 0,
            })
        } else {
            Ok(Lens {
                label: s[0..s.len() - 2].to_string(),
                action: Action::Add,
                focal_length: s.chars().last().unwrap().to_digit(10).unwrap() as usize,
            })
        }
    }
}

pub fn part2(input: &str) -> String {
    // There should be a better way to do this, but oh well
    let mut boxes: Vec<Vec<Lens>> = Vec::new();
    for _ in 0..256 {
        boxes.push(Vec::new());
    }

    for step in input.split(',') {
        let lens: Lens = step.parse().unwrap();
        let box_index = get_hash_value(&lens.label);

        match lens.action {
            Action::Add => {
                let mut found_matching_label = false;

                // Check if label is already in the box and replace if so
                for lens_in_box in boxes[box_index].iter_mut() {
                    if lens_in_box.label == lens.label {
                        *lens_in_box = lens.clone();
                        found_matching_label = true;
                        break;
                    }
                }

                // Add lens if the label is new
                if !found_matching_label {
                    boxes[box_index].push(lens.clone());
                }
            }
            Action::Remove => {
                // Happy with StackOverflow for pointing to this method :)
                boxes[box_index].retain(|e| e.label != lens.label);
            }
        }
    }

    let mut total = 0;
    for (index, boxx) in boxes.iter().enumerate() {
        for (lens_index, lens) in boxx.iter().enumerate() {
            // Make sure we don't multiply with 0
            total += (index + 1) * (lens_index + 1) * lens.focal_length;
        }
    }

    assert!(total == 262044, "Should be 262044");
    total.to_string()
}
