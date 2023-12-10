use std::collections::{HashMap, HashSet};

pub fn part1(input: &str) -> String {
    let mut total = 0;
    for line in input.lines() {
        let mut split_line = line.split(": ");
        let mut numbers = split_line.nth(1).unwrap().split(" | ");
        let mut good_numbers_vec: HashSet<String> = HashSet::new();
        for num in numbers.next().unwrap().split(' ') {
            if num.is_empty() {
                continue;
            } else {
                good_numbers_vec.insert(num.to_string());
            }
        }

        let mut score = 0;
        for num in numbers.next().unwrap().split(' ') {
            if num.is_empty() {
                continue;
            } else if good_numbers_vec.contains(num) {
                if score > 0 {
                    score *= 2;
                } else {
                    score += 1;
                }
            }
        }
        total += score;
    }
    assert!(total == 26914, "Should be 26914");
    total.to_string()
}

pub fn part2(input: &str) -> String {
    let mut original_scores: HashMap<usize, i32> = HashMap::new();
    for (index, line) in input.lines().enumerate() {
        let mut split_line = line.split(": ");
        let mut numbers = split_line.nth(1).unwrap().split(" | ");
        let mut good_numbers_vec: HashSet<String> = HashSet::new();
        for num in numbers.next().unwrap().split(' ') {
            if num.is_empty() {
                continue;
            } else {
                good_numbers_vec.insert(num.to_string());
            }
        }

        let mut score = 0;
        for num in numbers.next().unwrap().split(' ') {
            if num.is_empty() {
                continue;
            } else if good_numbers_vec.contains(num) {
                score += 1;
            }
        }
        original_scores.insert(index, score);
    }

    let mut card_wins: HashMap<usize, i32> = HashMap::new();
    for card_index in 0..input.lines().count() {
        let score: usize = *original_scores.get(&card_index).unwrap() as usize;
        let cards = card_wins
            .entry(card_index)
            .and_modify(|e| *e += 1)
            .or_insert(1)
            .to_owned();
        for new_card in card_index + 1..card_index + score + 1 {
            card_wins
                .entry(new_card)
                .and_modify(|e| *e += cards)
                .or_insert(cards);
        }
    }
    let total: i32 = card_wins.values().sum();
    assert!(total == 13080971, "Should be 13080971");
    total.to_string()
}
