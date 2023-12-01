pub fn parse_intcode(vals: Vec<&str>, input: i32) -> i32 {
    let mut pointer = 0;
    let mut values: Vec<i32> = vals.iter().map(|x| x.parse().unwrap()).collect();

    let mut output = -1;

    loop {
        let value = values[pointer];
        let opcode = value % 100;
        let mode_1 = value % 1000 / 100;
        let mode_2 = value % 10000 / 1000;
        let mode_3 = value % 100000 / 10000;

        match opcode {
            1 => {
                assert!(mode_3 == 0, "Should be mode 0");
                let final_position = values[pointer + 3] as usize;
                let val_1 = match mode_1 {
                    0 => values[values[pointer + 1] as usize],
                    1 => values[pointer + 1],
                    _ => panic!("Unsupported parameter mode '{}'", mode_1),
                };
                let val_2 = match mode_2 {
                    0 => values[values[pointer + 2] as usize],
                    1 => values[pointer + 2],
                    _ => panic!("Unsupported parameter mode '{}'", mode_2),
                };

                values[final_position] = val_1 + val_2;
                pointer += 4;
            }
            2 => {
                assert!(mode_3 == 0, "Should be mode 0");
                let final_position = values[pointer + 3] as usize;
                let val_1 = match mode_1 {
                    0 => values[values[pointer + 1] as usize],
                    1 => values[pointer + 1],
                    _ => panic!("Unsupported parameter mode '{}'", mode_1),
                };
                let val_2 = match mode_2 {
                    0 => values[values[pointer + 2] as usize],
                    1 => values[pointer + 2],
                    _ => panic!("Unsupported parameter mode '{}'", mode_2),
                };

                values[final_position] = val_1 * val_2;
                pointer += 4;
            }
            3 => {
                assert!(mode_3 == 0, "Should be mode 0");
                let final_position = values[pointer + 1] as usize;
                values[final_position] = input;
                pointer += 2;
            }
            4 => {
                let final_position = values[pointer + 1] as usize;
                output = values[final_position];
                pointer += 2;
            }
            5 => {
                let val_1 = match mode_1 {
                    0 => values[values[pointer + 1] as usize],
                    1 => values[pointer + 1],
                    _ => panic!("Unsupported parameter mode '{}'", mode_1),
                };

                if val_1 != 0 {
                    let val_2 = match mode_2 {
                        0 => values[values[pointer + 2] as usize],
                        1 => values[pointer + 2],
                        _ => panic!("Unsupported parameter mode '{}'", mode_2),
                    };
                    pointer = val_2 as usize;
                } else {
                    pointer += 3;
                }
            }
            6 => {
                let val_1 = match mode_1 {
                    0 => values[values[pointer + 1] as usize],
                    1 => values[pointer + 1],
                    _ => panic!("Unsupported parameter mode '{}'", mode_1),
                };

                if val_1 == 0 {
                    let val_2 = match mode_2 {
                        0 => values[values[pointer + 2] as usize],
                        1 => values[pointer + 2],
                        _ => panic!("Unsupported parameter mode '{}'", mode_2),
                    };
                    pointer = val_2 as usize;
                } else {
                    pointer += 3;
                }
            }
            7 => {
                assert!(mode_3 == 0, "Should be mode 0");
                let final_position = values[pointer + 3] as usize;
                let val_1 = match mode_1 {
                    0 => values[values[pointer + 1] as usize],
                    1 => values[pointer + 1],
                    _ => panic!("Unsupported parameter mode '{}'", mode_1),
                };
                let val_2 = match mode_2 {
                    0 => values[values[pointer + 2] as usize],
                    1 => values[pointer + 2],
                    _ => panic!("Unsupported parameter mode '{}'", mode_2),
                };
                if val_1 < val_2 {
                    values[final_position] = 1;
                } else {
                    values[final_position] = 0;
                }
                pointer += 4;
            }
            8 => {
                assert!(mode_3 == 0, "Should be mode 0");
                let final_position = values[pointer + 3] as usize;
                let val_1 = match mode_1 {
                    0 => values[values[pointer + 1] as usize],
                    1 => values[pointer + 1],
                    _ => panic!("Unsupported parameter mode '{}'", mode_1),
                };
                let val_2 = match mode_2 {
                    0 => values[values[pointer + 2] as usize],
                    1 => values[pointer + 2],
                    _ => panic!("Unsupported parameter mode '{}'", mode_2),
                };

                if val_1 == val_2 {
                    values[final_position] = 1;
                } else {
                    values[final_position] = 0;
                }
                pointer += 4;
            }
            99 => {
                if output > -1 {
                    return output;
                } else {
                    return values[0];
                }
            }
            _ => panic!("Unsupported opcode: '{}'", opcode),
        }
    }
}
