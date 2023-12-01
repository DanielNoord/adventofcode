use crate::intcode;

pub fn part1(input: &String) -> String {
    let mut values: Vec<&str> = input.split(",").collect();

    // Change noun and verb as per instructions
    values[1] = "12";
    values[2] = "2";

    let result = intcode::parse_intcode(values, 1);
    assert!(result == 3790645, "Should be 3790645");
    result.to_string()
}

pub fn part2(input: &String) -> String {
    let original_values: Vec<&str> = input.split(",").collect();

    fn get_result(original_values: Vec<&str>) -> u32 {
        for noun in 0..99 {
            for verb in 0..99 {
                let mut values = original_values.clone();
                let noun_str = noun.to_string();
                values[1] = &noun_str;
                let verb_str = verb.to_string();
                values[2] = &verb_str;
                if intcode::parse_intcode(values, 1) == 19690720 {
                    return 100 * noun + verb;
                }
            }
        }
        panic!("Should have found an answer");
    }

    let result = get_result(original_values);
    assert!(result == 6577, "Should be 6577");
    result.to_string()
}
