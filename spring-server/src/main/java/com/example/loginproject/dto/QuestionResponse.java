package com.example.loginproject.dto;

import com.example.loginproject.domain.Question;
import java.time.LocalDateTime;

public record QuestionResponse(
        Long id,
        String subject,
        String content,
        String authorUsername,
        String authorName,
        LocalDateTime createdAt,
        LocalDateTime updatedAt
) {

    public static QuestionResponse from(Question question) {
        String authorUsername = question.getAuthor() == null ? null : question.getAuthor().getUsername();
        String authorName = question.getAuthor() == null ? "작성자 없음" : question.getAuthor().getName();

        return new QuestionResponse(
                question.getId(),
                question.getSubject(),
                question.getContent(),
                authorUsername,
                authorName,
                question.getCreatedAt(),
                question.getUpdatedAt()
        );
    }
}
