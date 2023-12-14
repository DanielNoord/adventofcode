fn transpose_pattern(input: Vec<String>) -> Vec<String> {
    let max_x = input.len();

    // Get a vector of char vectors so we can index each row easily
    let lines_as_chars: Vec<Vec<char>> =
        input.iter().map(|e| e.chars().collect()).collect();

    let mut new_lines: Vec<String> = Vec::new();
    for x_coord in 0..max_x {
        new_lines.push(String::new());
        for line in lines_as_chars.iter() {
            new_lines[x_coord].push(line[x_coord]);
        }
    }

    new_lines
}

pub fn part1(input: &str) -> String {
    let mut total = 0;
    let input: Vec<String> = Vec::from_iter(input.lines().map(|e| e.to_string()));
    let mut transposed_input = transpose_pattern(input);
    let column_length = transposed_input[0].len() as u32;

    for column in transposed_input.iter_mut() {
        let mut rounded_rocks: u32 = 0;
        let mut last_cube_rock: usize = usize::MIN;
        for (index, char) in column.char_indices() {
            match char {
                '.' => continue,
                '#' => {
                    if rounded_rocks > 0 {
                        for i in 0..rounded_rocks {
                            total += column_length - last_cube_rock as u32 - i;
                        }
                    }
                    last_cube_rock = index + 1;
                    rounded_rocks = 0;
                }
                'O' => rounded_rocks += 1,
                _ => panic!("{}", char),
            }
        }
        if rounded_rocks > 0 {
            for i in 0..rounded_rocks {
                total += column_length - last_cube_rock as u32 - i;
            }
        }
    }

    // assert!(total == 113424, "Should be 113424 {total}");
    total.to_string()
}

pub fn part2(_input: &str) -> String {
    let total = 0;
    total.to_string()
}
