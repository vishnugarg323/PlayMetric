package org.playmetric.repository;

import org.playmetric.model.AdsEvent;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AdsEventRepository extends MongoRepository<AdsEvent, String> {}
