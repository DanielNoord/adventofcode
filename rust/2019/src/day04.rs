fn is_valid(num: u32) -> bool {
    let mut doubles = false;
    let mut prev = -1;
    for inner in num.to_string().chars() {
        let inner_val: i32 = inner.to_string().parse().expect("");
        if !doubles && prev == inner_val {
            doubles = true;
        }
        if inner_val < prev {
            return false;
        }
        prev = inner_val;
    }
    doubles
}

fn is_valid_part2(num: u32) -> bool {
    let mut doubles = false;
    let mut in_double = 0;
    let mut prev = -1;
    for inner in num.to_string().chars() {
        let inner_val: i32 = inner.to_string().parse().expect("");
        if prev == inner_val {
            in_double += 1;
        } else {
            if !doubles && in_double == 1 {
                doubles = true;
            }
            in_double = 0;
        }

        if inner_val < prev {
            return false;
        }
        prev = inner_val;
    }

    if in_double == 1 {
        return true;
    }
    doubles
}

pub fn part1(input: &str) -> String {
    let num_vec: Vec<&str> = input.split('-').collect();
    let mut nums = num_vec.iter();
    let lowest: u32 = nums.next().unwrap().parse().expect("");
    let highest: u32 = nums.next().unwrap().parse().expect("");

    let mut matches = 0;
    for val in lowest..highest {
        if is_valid(val) {
            matches += 1;
        }
    }

    assert!(matches == 1686, "Should be 1686");
    matches.to_string()
}

pub fn part2(input: &str) -> String {
    let num_vec: Vec<&str> = input.split('-').collect();
    let mut nums = num_vec.iter();
    let lowest: u32 = nums.next().unwrap().parse().expect("");
    let highest: u32 = nums.next().unwrap().parse().expect("");

    let mut matches = 0;
    for val in lowest..highest {
        if is_valid_part2(val) {
            matches += 1;
        }
    }

    assert!(matches == 1145, "Should be 1145");
    matches.to_string()
}
