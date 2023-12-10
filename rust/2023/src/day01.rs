fn get_first_digit(line: &str) -> char {
    for char in line.chars() {
        if char.is_ascii_digit() {
            return char;
        }
    }
    panic!("Should have found a digit")
}

fn get_last_digit(line: &str) -> char {
    for char in line.chars().rev() {
        if char.is_ascii_digit() {
            return char;
        }
    }
    panic!("Should have found a digit")
}

fn get_letter_number(line: &str, mut index: usize) -> String {
    let mut to_replace = "";
    let mut new_value = "";

    let mut potential_index = line.find("one").unwrap_or(line.len());
    if potential_index <= index {
        index = potential_index;
        to_replace = "one";
        new_value = "1";
    }
    potential_index = line.find("two").unwrap_or(line.len());
    if potential_index <= index {
        index = potential_index;
        to_replace = "two";
        new_value = "2";
    }
    potential_index = line.find("three").unwrap_or(line.len());
    if potential_index <= index {
        index = potential_index;
        to_replace = "three";
        new_value = "3";
    }
    potential_index = line.find("four").unwrap_or(line.len());
    if potential_index <= index {
        index = potential_index;
        to_replace = "four";
        new_value = "4";
    }
    potential_index = line.find("five").unwrap_or(line.len());
    if potential_index <= index {
        index = potential_index;
        to_replace = "five";
        new_value = "5";
    }
    potential_index = line.find("six").unwrap_or(line.len());
    if potential_index <= index {
        index = potential_index;
        to_replace = "six";
        new_value = "6";
    }
    potential_index = line.find("seven").unwrap_or(line.len());
    if potential_index <= index {
        index = potential_index;
        to_replace = "seven";
        new_value = "7";
    }
    potential_index = line.find("eight").unwrap_or(line.len());
    if potential_index <= index {
        index = potential_index;
        to_replace = "eight";
        new_value = "8";
    }
    potential_index = line.find("nine").unwrap_or(line.len());
    if potential_index <= index {
        to_replace = "nine";
        new_value = "9";
    }

    if !to_replace.is_empty() {
        return line.replacen(to_replace, new_value, 1);
    }

    line.to_string()
}

fn get_letter_number_last(line: &str) -> String {
    let mut to_replace = "";
    let mut new_value = "";
    let mut index = usize::MIN;

    let mut potential_index = line.rfind("one").unwrap_or(usize::MIN);
    if potential_index >= index {
        index = potential_index;
        to_replace = "one";
        new_value = "1";
    }
    potential_index = line.rfind("two").unwrap_or(usize::MIN);
    if potential_index >= index {
        index = potential_index;
        to_replace = "two";
        new_value = "2";
    }
    potential_index = line.rfind("three").unwrap_or(usize::MIN);
    if potential_index >= index {
        index = potential_index;
        to_replace = "three";
        new_value = "3";
    }
    potential_index = line.rfind("four").unwrap_or(usize::MIN);
    if potential_index >= index {
        index = potential_index;
        to_replace = "four";
        new_value = "4";
    }
    potential_index = line.rfind("five").unwrap_or(usize::MIN);
    if potential_index >= index {
        index = potential_index;
        to_replace = "five";
        new_value = "5";
    }
    potential_index = line.rfind("six").unwrap_or(usize::MIN);
    if potential_index >= index {
        index = potential_index;
        to_replace = "six";
        new_value = "6";
    }
    potential_index = line.rfind("seven").unwrap_or(usize::MIN);
    if potential_index >= index {
        index = potential_index;
        to_replace = "seven";
        new_value = "7";
    }
    potential_index = line.rfind("eight").unwrap_or(usize::MIN);
    if potential_index >= index {
        index = potential_index;
        to_replace = "eight";
        new_value = "8";
    }
    potential_index = line.rfind("nine").unwrap_or(usize::MIN);
    if potential_index >= index {
        to_replace = "nine";
        new_value = "9";
    }

    if !to_replace.is_empty() {
        return line.replace(to_replace, new_value);
    }

    line.to_string()
}

fn replace_digits(line: &str) -> String {
    let mut first_index = line.len();
    for (index, char) in line.char_indices() {
        if char.is_ascii_digit() {
            first_index = index;
            break;
        }
    }
    let mut replline = get_letter_number(line, first_index);
    replline = get_letter_number_last(&replline);
    replline.to_owned()
}

pub fn part1(input: &str) -> String {
    let mut total: u32 = 0;
    for line in input.lines() {
        let mut number = String::new();
        number.push(get_first_digit(line));
        number.push(get_last_digit(line));

        let value: u32 = number.parse().unwrap();
        total += value
    }
    assert!(total == 55712, "Should be 55712");
    total.to_string()
}

pub fn part2(input: &str) -> String {
    let mut total: u32 = 0;
    for line in input.lines() {
        let mut number = String::new();
        let line = &replace_digits(line);
        number.push(get_first_digit(line));
        number.push(get_last_digit(line));

        let value: u32 = number.parse().unwrap();
        total += value
    }
    assert!(total == 55413, "Should be 55413");
    total.to_string()
}
