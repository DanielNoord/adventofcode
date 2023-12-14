use std::collections::HashMap;

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

    // Transpose the graph so we can easily iterate through each column
    let mut transposed_input = transpose_pattern(input);
    let column_length = transposed_input[0].len() as u32;

    for column in transposed_input.iter_mut() {
        // Store how many rounded rocks we saw since the last rounded rock
        let mut rounded_rocks: u32 = 0;
        let mut last_cube_rock: usize = usize::MIN;

        for (index, char) in column.char_indices() {
            match char {
                '.' => continue,
                '#' => {
                    for i in 0..rounded_rocks {
                        total += column_length - last_cube_rock as u32 - i;
                    }
                    // Take the next index as that's is what we eventually need to calculate
                    last_cube_rock = index + 1;
                    rounded_rocks = 0;
                }
                'O' => rounded_rocks += 1,
                _ => panic!("{}", char),
            }
        }

        // Don't forget to check for any remaining rocks
        for i in 0..rounded_rocks {
            total += column_length - last_cube_rock as u32 - i;
        }
    }

    assert!(total == 113424, "Should be 113424 {total}");
    total.to_string()
}

fn move_rocks(mut graph: Vec<String>) -> Vec<String> {
    let column_length = graph[0].len();
    for column in graph.iter_mut() {
        let mut new_column = String::new();
        let mut rounded_rocks: u32 = 0;
        let mut last_cube_rock: usize = usize::MIN;
        for (index, char) in column.char_indices() {
            match char {
                '.' => continue,
                '#' => {
                    for _ in 0..rounded_rocks {
                        new_column.push('O');
                    }

                    for _ in last_cube_rock..index - rounded_rocks as usize {
                        new_column.push('.');
                    }

                    new_column.push('#');

                    last_cube_rock = index + 1;
                    rounded_rocks = 0;
                }
                'O' => rounded_rocks += 1,
                _ => panic!("{}", char),
            }
        }
        for _ in 0..rounded_rocks {
            new_column.push('O');
        }
        for _ in last_cube_rock..column_length - rounded_rocks as usize {
            new_column.push('.');
        }
        *column = new_column;
    }
    graph
}

pub fn part2(input: &str) -> String {
    let mut total = 0;
    let mut graph: Vec<String> = Vec::from_iter(input.lines().map(|e| e.to_string()));

    let mut seen_maps: HashMap<Vec<String>, usize> = HashMap::new();

    let mut cycles_left = 1000000000;
    let mut cycle: usize = 0;

    loop {
        cycle += 1;
        if cycles_left == 0 {
            break;
        } else if let Some(entry) = seen_maps.get(&graph) {
            cycles_left %= cycle - entry;
        }
        cycles_left -= 1;

        // Make sure we count cycle :)
        seen_maps.insert(graph.clone(), cycle);

        // Tranpose so North is left
        graph = transpose_pattern(graph);
        graph = move_rocks(graph);

        // Transpose back so West is left again
        graph = transpose_pattern(graph);
        graph = move_rocks(graph);

        // Flip and transpose so South is left
        graph.reverse();
        graph = transpose_pattern(graph);
        graph = move_rocks(graph);

        // Flip and transpose so East is left
        graph.reverse();
        graph = transpose_pattern(graph);
        graph = move_rocks(graph);

        // Flip and reverse again so West is left and we're back in normal orientation
        graph.reverse();
        graph = graph
            .iter_mut()
            .map(|e| e.chars().rev().collect::<String>())
            .collect::<Vec<String>>();
    }

    // Calculate the stress on the North beam, assuming North is at the top again
    let column_length = graph[0].len();
    for (index, column) in graph.iter().enumerate() {
        total += column.chars().filter(|e| e == &'O').count() * (column_length - index);
    }

    assert!(total == 96003, "Should be 96003 {total}");
    total.to_string()
}
