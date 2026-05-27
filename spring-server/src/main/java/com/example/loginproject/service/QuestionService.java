package com.example.loginproject.service;

import com.example.loginproject.domain.Member;
import com.example.loginproject.domain.Question;
import com.example.loginproject.dto.QuestionCreateRequest;
import com.example.loginproject.dto.QuestionResponse;
import com.example.loginproject.dto.QuestionUpdateRequest;
import com.example.loginproject.repository.MemberRepository;
import com.example.loginproject.repository.QuestionRepository;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class QuestionService {

    private final QuestionRepository questionRepository;
    private final MemberRepository memberRepository;

    public List<QuestionResponse> findAll() {
        return questionRepository.findAll()
                .stream()
                .map(QuestionResponse::from)
                .toList();
    }

    public QuestionResponse findById(Long id) {
        return QuestionResponse.from(getQuestion(id));
    }

    public QuestionUpdateRequest findUpdateForm(Long id, Authentication authentication) {
        Question question = getQuestion(id);
        validateModifyPermission(question, authentication);
        return new QuestionUpdateRequest(question.getSubject(), question.getContent());
    }

    public boolean canModify(Long id, Authentication authentication) {
        Question question = getQuestion(id);
        return hasModifyPermission(question, authentication);
    }

    @Transactional
    public Long create(QuestionCreateRequest request, String username) {
        Member author = memberRepository.findByUsername(username)
                .orElseThrow(() -> new IllegalArgumentException("로그인 회원을 찾을 수 없습니다."));

        Question question = new Question(request.subject(), request.content(), author);
        return questionRepository.save(question).getId();
    }

    @Transactional
    public void update(Long id, QuestionUpdateRequest request, Authentication authentication) {
        Question question = getQuestion(id);
        validateModifyPermission(question, authentication);
        question.update(request.subject(), request.content());
    }

    @Transactional
    public void delete(Long id, Authentication authentication) {
        Question question = getQuestion(id);
        validateModifyPermission(question, authentication);
        questionRepository.delete(question);
    }

    private Question getQuestion(Long id) {
        return questionRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("게시글을 찾을 수 없습니다."));
    }

    private void validateModifyPermission(Question question, Authentication authentication) {
        if (!hasModifyPermission(question, authentication)) {
            throw new IllegalStateException("게시글을 수정하거나 삭제할 권한이 없습니다.");
        }
    }

    private boolean hasModifyPermission(Question question, Authentication authentication) {
        if (authentication == null || !authentication.isAuthenticated()) {
            return false;
        }

        boolean admin = isAdmin(authentication);
        if (!question.hasAuthor()) {
            return admin;
        }

        return question.isWrittenBy(authentication.getName());
    }

    private boolean isAdmin(Authentication authentication) {
        return authentication.getAuthorities()
                .stream()
                .map(GrantedAuthority::getAuthority)
                .anyMatch("ROLE_ADMIN"::equals);
    }
}
