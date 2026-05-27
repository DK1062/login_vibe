package com.example.loginproject.dto;

import com.example.loginproject.domain.Member;
import com.example.loginproject.domain.Role;
import java.time.LocalDateTime;

public record MemberResponse(
        Long id,
        String username,
        String name,
        Role role,
        LocalDateTime createdAt
) {

    public static MemberResponse from(Member member) {
        return new MemberResponse(
                member.getId(),
                member.getUsername(),
                member.getName(),
                member.getRole(),
                member.getCreatedAt()
        );
    }
}
