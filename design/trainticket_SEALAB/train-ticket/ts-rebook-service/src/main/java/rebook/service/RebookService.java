package rebook.service;

import org.springframework.http.HttpHeaders;
import rebook.domain.RebookInfo;
import rebook.domain.RebookResult;

public interface RebookService {
    RebookResult rebook(RebookInfo info, String loginId, String loginToken, HttpHeaders headers);
    RebookResult payDifference(RebookInfo info, String loginId, String loginToken, HttpHeaders headers);
}
