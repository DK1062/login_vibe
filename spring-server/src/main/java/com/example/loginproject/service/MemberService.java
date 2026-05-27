package com.example.loginproject.service;

import com.example.loginproject.domain.Member;
import com.example.loginproject.domain.Role;
import com.example.loginproject.dto.MemberResponse;
import com.example.loginproject.dto.MemberSignupRequest;
import com.example.loginproject.repository.MemberRepository;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class MemberService {

    private final MemberRepository memberRepository;
    private final PasswordEncoder passwordEncoder;

    @Transactional
    public Long signup(MemberSignupRequest request) {
        validateDuplicateUsername(request.username());

        Member member = new Member(
                request.username(),
                passwordEncoder.encode(request.password()),
                request.name(),
                Role.USER
        );

        return memberRepository.save(member).getId();
    }

    public List<MemberResponse> findAllMembers() {
        return memberRepository.findAll()
                .stream()
                .map(MemberResponse::from)
                .toList();
    }

    private void validateDuplicateUsername(String username) {
        if (memberRepository.existsByUsername(username)) {
            throw new IllegalArgumentException("이미 사용 중인 아이디입니다.");
        }
    }
}
